from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
CODE_BLOCK_RE = re.compile(r"```.+?```|`[^`]+`", re.DOTALL)
WHITESPACE_RE = re.compile(r"\s+")
DEFAULT_SOURCE = "discord"


@dataclass(slots=True)
class ScrapeStats:
    files_processed: int = 0
    messages_written: int = 0
    channels_seen: int = 0
    threads_seen: int = 0
    authors_seen: int = 0
    attachments_seen: int = 0
    embeds_seen: int = 0
    replies_seen: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert DiscordChatExporter JSON exports into a rich CSV dataset."
    )
    parser.add_argument(
        "input",
        help="Path to a Discord JSON export file or directory containing JSON exports.",
    )
    parser.add_argument(
        "output",
        help="Path to the output CSV file.",
    )
    parser.add_argument(
        "--glob",
        default="*.json",
        help="Glob used when the input path is a directory. Default: %(default)s",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Keep rows even if the message has no textual content, attachments, or embeds.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    files = collect_input_files(input_path, args.glob)
    if not files:
        raise SystemExit(f"No JSON files found in: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    stats = ScrapeStats(files_processed=len(files))
    seen_channels: set[str] = set()
    seen_threads: set[str] = set()
    seen_authors: set[str] = set()

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_columns())
        writer.writeheader()

        for file_path in files:
            payload = load_json(file_path)
            for row in build_rows(file_path, payload, args.include_empty):
                writer.writerow(row)
                stats.messages_written += 1
                if row["channel_id"]:
                    seen_channels.add(row["channel_id"])
                if row["thread_id"]:
                    seen_threads.add(row["thread_id"])
                if row["author_id"]:
                    seen_authors.add(row["author_id"])
                stats.attachments_seen += int(row["attachment_count"])
                stats.embeds_seen += int(row["embed_count"])
                stats.replies_seen += int(bool(row["reply_to_message_id"]))

    stats.channels_seen = len(seen_channels)
    stats.threads_seen = len(seen_threads)
    stats.authors_seen = len(seen_authors)

    print_summary(output_path, stats)
    return 0


def collect_input_files(input_path: Path, pattern: str) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if input_path.is_dir():
        return sorted(path for path in input_path.rglob(pattern) if path.is_file())
    return []


def load_json(file_path: Path) -> Any:
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_rows(file_path: Path, payload: Any, include_empty: bool) -> list[dict[str, str]]:
    export = normalize_export_payload(payload)
    metadata = extract_export_metadata(export, file_path)
    messages = export.get("messages") or []

    rows: list[dict[str, str]] = []
    for index, message in enumerate(messages):
        row = build_message_row(message, metadata, file_path, index)
        if include_empty or should_keep_row(row):
            rows.append(row)
    return rows


def normalize_export_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list):
        return {"messages": payload}
    raise ValueError("Unsupported JSON structure. Expected dict or list.")


def extract_export_metadata(export: dict[str, Any], file_path: Path) -> dict[str, str]:
    guild = first_dict(export, "guild", "server")
    channel = first_dict(export, "channel")

    server_id = string_value(guild, "id")
    server_name = first_non_empty(
        string_value(guild, "name"),
        string_value(export, "guildName"),
        string_value(export, "serverName"),
    )
    channel_id = first_non_empty(
        string_value(channel, "id"),
        string_value(export, "channelId"),
    )
    channel_name = first_non_empty(
        string_value(channel, "name"),
        string_value(export, "channelName"),
        file_path.stem,
    )
    channel_type = first_non_empty(
        string_value(channel, "type"),
        string_value(export, "channelType"),
        "text",
    )

    return {
        "server_id": server_id,
        "server_name": server_name,
        "channel_id": channel_id,
        "channel_name": channel_name,
        "channel_type": channel_type,
        "export_file": str(file_path),
        "export_name": file_path.name,
    }


def build_message_row(
    message: dict[str, Any],
    metadata: dict[str, str],
    file_path: Path,
    index: int,
) -> dict[str, str]:
    author = first_dict(message, "author")
    reference = first_dict(message, "reference", "referencedMessage")
    thread = first_dict(message, "thread")
    reactions = message.get("reactions") or []
    attachments = message.get("attachments") or []
    embeds = message.get("embeds") or []
    mentions = message.get("mentions") or []
    mention_roles = message.get("mentionRoles") or message.get("roleMentions") or []
    stickers = message.get("stickers") or []

    content_raw = first_non_empty(
        string_value(message, "content"),
        string_value(message, "message"),
        string_value(message, "text"),
    )
    content_clean = clean_text(content_raw)

    message_id = first_non_empty(string_value(message, "id"), derive_message_id(file_path, index, content_raw))
    thread_id = first_non_empty(
        string_value(thread, "id"),
        string_value(message, "threadId"),
        string_value(reference, "threadId"),
    )
    thread_name = first_non_empty(
        string_value(thread, "name"),
        string_value(message, "threadName"),
    )
    reply_to_message_id = first_non_empty(
        string_value(message, "replyTo"),
        string_value(message, "replyToMessageId"),
        string_value(reference, "messageId"),
        string_value(reference, "id"),
    )

    attachment_urls = flatten_values(attachments, ("url", "proxyUrl"))
    attachment_names = flatten_values(attachments, ("fileName", "filename", "name"))
    attachment_types = flatten_values(attachments, ("contentType", "mediaType", "extension"))
    embed_titles = flatten_values(embeds, ("title",))
    embed_urls = flatten_values(embeds, ("url",))
    embed_descriptions = flatten_values(embeds, ("description",))
    reaction_emojis = join_list([extract_reaction_name(reaction) for reaction in reactions])
    reaction_count = sum(safe_int(first_non_empty(reaction.get("count"), reaction.get("total"))) for reaction in reactions)

    mention_user_ids = join_list([string_value(mention, "id") for mention in mentions])
    mention_usernames = join_list(
        [
            first_non_empty(
                string_value(mention, "name"),
                string_value(mention, "username"),
                string_value(mention, "nickname"),
            )
            for mention in mentions
        ]
    )
    mention_role_ids = join_list(normalize_list(mention_roles))

    author_id = first_non_empty(string_value(author, "id"), string_value(message, "authorId"))
    author_name = first_non_empty(
        string_value(author, "name"),
        string_value(author, "username"),
        string_value(message, "authorName"),
    )
    author_global_name = first_non_empty(
        string_value(author, "globalName"),
        string_value(author, "displayName"),
        string_value(author, "nickname"),
    )

    created_at = normalize_timestamp(
        first_non_empty(
            string_value(message, "timestamp"),
            string_value(message, "createdAt"),
            string_value(message, "date"),
        )
    )
    edited_at = normalize_timestamp(
        first_non_empty(
            string_value(message, "editedTimestamp"),
            string_value(message, "editedAt"),
        )
    )

    conversation_key = build_conversation_key(
        metadata["server_id"],
        metadata["channel_id"],
        thread_id,
        reply_to_message_id,
        message_id,
    )
    source_path = first_non_empty(string_value(message, "messageLink"), string_value(message, "url"))
    document_id = build_document_id(DEFAULT_SOURCE, metadata["channel_id"], thread_id, message_id)
    entity_people, entity_tools, entity_topics = infer_entities(content_clean, mention_usernames, metadata["channel_name"])

    char_count = len(content_clean)
    word_count = count_words(content_clean)
    row = {
        "source": DEFAULT_SOURCE,
        "export_file": metadata["export_file"],
        "export_name": metadata["export_name"],
        "server_id": metadata["server_id"],
        "server_name": metadata["server_name"],
        "channel_id": metadata["channel_id"],
        "channel_name": metadata["channel_name"],
        "channel_type": metadata["channel_type"],
        "thread_id": thread_id,
        "thread_name": thread_name,
        "message_id": message_id,
        "message_type": first_non_empty(string_value(message, "type"), "default"),
        "message_url": source_path,
        "author_id": author_id,
        "author_name": author_name,
        "author_global_name": author_global_name,
        "author_is_bot": bool_str(bool(author.get("isBot") or author.get("bot"))),
        "created_at": created_at,
        "edited_at": edited_at,
        "reply_to_message_id": reply_to_message_id,
        "content_raw": content_raw,
        "content_clean": content_clean,
        "char_count": str(char_count),
        "word_count": str(word_count),
        "tokens_estimate": str(estimate_tokens(content_clean)),
        "language_hint": infer_language_hint(content_clean),
        "has_code_block": bool_str(bool(CODE_BLOCK_RE.search(content_raw))),
        "has_link": bool_str(bool(URL_RE.search(content_raw))),
        "has_attachment": bool_str(bool(attachments)),
        "has_embed": bool_str(bool(embeds)),
        "mentioned_everyone": bool_str(bool(message.get("mentionEveryone"))),
        "mentions_user_ids": mention_user_ids,
        "mentions_usernames": mention_usernames,
        "mentions_role_ids": mention_role_ids,
        "reaction_count": str(reaction_count),
        "reaction_emojis": reaction_emojis,
        "attachment_count": str(len(attachments)),
        "attachment_urls": attachment_urls,
        "attachment_names": attachment_names,
        "attachment_types": attachment_types,
        "embed_count": str(len(embeds)),
        "embed_titles": embed_titles,
        "embed_urls": embed_urls,
        "embed_descriptions": embed_descriptions,
        "sticker_count": str(len(stickers)),
        "sticker_names": flatten_values(stickers, ("name", "fileName")),
        "reference_message_id": first_non_empty(string_value(reference, "id"), string_value(reference, "messageId")),
        "conversation_key": conversation_key,
        "document_id": document_id,
        "entity_people": entity_people,
        "entity_tools": entity_tools,
        "entity_topics": entity_topics,
    }
    return row


def should_keep_row(row: dict[str, str]) -> bool:
    return any(
        (
            row["content_clean"],
            row["attachment_count"] != "0",
            row["embed_count"] != "0",
            row["sticker_count"] != "0",
        )
    )


def csv_columns() -> list[str]:
    return [
        "source",
        "export_file",
        "export_name",
        "server_id",
        "server_name",
        "channel_id",
        "channel_name",
        "channel_type",
        "thread_id",
        "thread_name",
        "message_id",
        "message_type",
        "message_url",
        "author_id",
        "author_name",
        "author_global_name",
        "author_is_bot",
        "created_at",
        "edited_at",
        "reply_to_message_id",
        "content_raw",
        "content_clean",
        "char_count",
        "word_count",
        "tokens_estimate",
        "language_hint",
        "has_code_block",
        "has_link",
        "has_attachment",
        "has_embed",
        "mentioned_everyone",
        "mentions_user_ids",
        "mentions_usernames",
        "mentions_role_ids",
        "reaction_count",
        "reaction_emojis",
        "attachment_count",
        "attachment_urls",
        "attachment_names",
        "attachment_types",
        "embed_count",
        "embed_titles",
        "embed_urls",
        "embed_descriptions",
        "sticker_count",
        "sticker_names",
        "reference_message_id",
        "conversation_key",
        "document_id",
        "entity_people",
        "entity_tools",
        "entity_topics",
    ]


def clean_text(value: str) -> str:
    if not value:
        return ""
    cleaned = value.replace("\u00a0", " ").replace("\r", "\n")
    cleaned = WHITESPACE_RE.sub(" ", cleaned).strip()
    return cleaned


def normalize_timestamp(value: str) -> str:
    if not value:
        return ""
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def extract_reaction_name(reaction: Any) -> str:
    if isinstance(reaction, str):
        return reaction
    if isinstance(reaction, dict):
        emoji = reaction.get("emoji")
        if isinstance(emoji, dict):
            return first_non_empty(string_value(emoji, "name"), string_value(emoji, "id"))
        return first_non_empty(string_value(reaction, "emoji"), string_value(reaction, "name"))
    return ""


def flatten_values(items: list[Any], keys: tuple[str, ...]) -> str:
    values: list[str] = []
    for item in items:
        if isinstance(item, dict):
            for key in keys:
                value = item.get(key)
                if value not in (None, ""):
                    values.append(str(value))
                    break
        elif item not in (None, ""):
            values.append(str(item))
    return join_list(values)


def build_conversation_key(
    server_id: str,
    channel_id: str,
    thread_id: str,
    reply_to_message_id: str,
    message_id: str,
) -> str:
    scope = first_non_empty(thread_id, reply_to_message_id, message_id)
    return "::".join(part for part in (server_id, channel_id, scope) if part)


def build_document_id(source: str, channel_id: str, thread_id: str, message_id: str) -> str:
    return "::".join(part for part in (source, channel_id, thread_id, message_id) if part)


def derive_message_id(file_path: Path, index: int, content: str) -> str:
    digest = hashlib.sha1(f"{file_path}:{index}:{content}".encode("utf-8")).hexdigest()[:16]
    return f"derived-{digest}"


def infer_entities(content: str, mention_usernames: str, channel_name: str) -> tuple[str, str, str]:
    people = sorted({value for value in split_joined_values(mention_usernames) if value})
    tool_candidates = {
        token
        for token in re.findall(r"\b[A-Z][A-Za-z0-9_.+-]{1,}\b", content)
        if any(char.isupper() for char in token[1:]) or token in {"API", "SDK", "CLI", "RN", "AI"}
    }
    topic_counts = Counter(
        token.lower()
        for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]{3,}\b", content)
        if token.lower() not in STOPWORDS
    )
    topics = [token for token, _ in topic_counts.most_common(8)]
    if channel_name:
        topics.insert(0, channel_name.lstrip("#").lower())
    return join_list(people), join_list(sorted(tool_candidates)[:12]), join_list(dedupe_preserve_order(topics)[:12])


def infer_language_hint(content: str) -> str:
    if not content:
        return ""
    polish_markers = {"się", "żeby", "jest", "oraz", "który"}
    lowered = {token.lower() for token in re.findall(r"\b\w+\b", content)}
    if lowered & polish_markers:
        return "pl"
    return "en"


def count_words(content: str) -> int:
    return len(re.findall(r"\b\w+\b", content))


def estimate_tokens(content: str) -> int:
    if not content:
        return 0
    return max(1, len(content) // 4)


def print_summary(output_path: Path, stats: ScrapeStats) -> None:
    print(f"Wrote CSV: {output_path}")
    print(f"Files processed: {stats.files_processed}")
    print(f"Messages written: {stats.messages_written}")
    print(f"Channels seen: {stats.channels_seen}")
    print(f"Threads seen: {stats.threads_seen}")
    print(f"Authors seen: {stats.authors_seen}")
    print(f"Attachments seen: {stats.attachments_seen}")
    print(f"Embeds seen: {stats.embeds_seen}")
    print(f"Reply links seen: {stats.replies_seen}")


def first_dict(container: dict[str, Any], *keys: str) -> dict[str, Any]:
    for key in keys:
        value = container.get(key)
        if isinstance(value, dict):
            return value
    return {}


def string_value(container: dict[str, Any], key: str) -> str:
    value = container.get(key)
    if value is None:
        return ""
    return str(value)


def first_non_empty(*values: Any) -> str:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def normalize_list(values: Any) -> list[str]:
    if isinstance(values, list):
        return [str(value) for value in values if value not in (None, "")]
    if values in (None, ""):
        return []
    return [str(values)]


def join_list(values: list[str]) -> str:
    return " | ".join(dedupe_preserve_order([value.strip() for value in values if value and value.strip()]))


def split_joined_values(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


STOPWORDS = {
    "about",
    "also",
    "been",
    "from",
    "have",
    "just",
    "more",
    "that",
    "them",
    "they",
    "this",
    "with",
    "your",
    "there",
    "what",
    "when",
    "where",
    "which",
    "would",
    "should",
    "could",
    "into",
    "works",
    "work",
    "need",
    "does",
    "dont",
    "using",
    "used",
    "user",
    "team",
    "thanks",
    "thank",
    "hello",
    "channel",
    "message",
    "discord",
}


if __name__ == "__main__":
    raise SystemExit(main())
