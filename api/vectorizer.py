from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any


DEFAULT_LOCATION = "us-east4"
DEFAULT_EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"
DEFAULT_CORPUS_NAME = "gemelius corpus"


class VectorizerError(Exception):
    """Base error for Vertex RAG integration."""


class VectorizerConfigError(VectorizerError):
    """Raised when required config is missing."""


class CorpusProvisionError(VectorizerError):
    """Raised when a per-person corpus cannot be created or resolved."""


class DocumentImportError(VectorizerError):
    """Raised when a document cannot be uploaded to Vertex RAG."""


@dataclass(slots=True)
class VectorizerSettings:
    project_id: str
    location: str = DEFAULT_LOCATION
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    corpus_name: str = DEFAULT_CORPUS_NAME
    chunk_size: int = 512
    chunk_overlap: int = 100
    max_embedding_requests_per_min: int = 1_000

    @classmethod
    def from_env(cls) -> "VectorizerSettings":
        project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise VectorizerConfigError(
                "Missing GCP project id. Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT."
            )

        return cls(
            project_id=project_id,
            location=os.getenv("GCP_LOCATION", DEFAULT_LOCATION),
            embedding_model=os.getenv("VERTEX_RAG_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
            corpus_name=os.getenv("VERTEX_RAG_CORPUS_NAME", DEFAULT_CORPUS_NAME),
            chunk_size=int(os.getenv("VERTEX_RAG_CHUNK_SIZE", "512")),
            chunk_overlap=int(os.getenv("VERTEX_RAG_CHUNK_OVERLAP", "100")),
            max_embedding_requests_per_min=int(
                os.getenv("VERTEX_RAG_EMBEDDING_RPM", "1000")
            ),
        )


@dataclass(slots=True)
class UploadResult:
    corpus_name: str
    display_name: str
    source_path: str
    operation_id: str | None = None
    rag_file_id: str | None = None


@dataclass(slots=True)
class SearchResult:
    text: str
    source_uri: str | None = None
    score: float | None = None
    raw_chunk: Any | None = None


class VectorizerService:
    def __init__(self, settings: VectorizerSettings | None = None) -> None:
        self.settings = settings or VectorizerSettings.from_env()

    @cached_property
    def _rag_module(self) -> Any:
        try:
            import google.auth
            import vertexai
            from vertexai import rag
            from google.oauth2.credentials import Credentials
            from tools import get_google_access_token
        except ImportError as exc:
            raise VectorizerConfigError(
                "vertexai is not installed. Add google-cloud-aiplatform to api/requirements.txt."
            ) from exc

        creds = Credentials(token=get_google_access_token())
        vertexai.init(project=self.settings.project_id, location=self.settings.location, credentials=creds)

        # Monkey-patch google.auth.default so the Vertex AI SDK always uses
        # our access-token credentials instead of Application Default Credentials.
        _original_default = google.auth.default

        def _patched_default(*args: Any, **kwargs: Any) -> tuple:
            return creds, self.settings.project_id

        google.auth.default = _patched_default  # type: ignore[assignment]
        return rag

    def corpus_display_name(self) -> str:
        return self.settings.corpus_name

    def ensure_corpus(self) -> str:
        display_name = self.corpus_display_name()
        existing_corpus = self._find_corpus_by_display_name(display_name)
        if existing_corpus is not None:
            return self._corpus_name(existing_corpus)

        rag = self._rag_module
        try:
            corpus = rag.create_corpus(
                display_name=display_name,
                backend_config=rag.RagVectorDbConfig(
                    rag_embedding_model_config=rag.RagEmbeddingModelConfig(
                        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                            publisher_model=self.settings.embedding_model
                        )
                    )
                ),
            )
        except Exception as exc:
            raise CorpusProvisionError(
                "Unable to create RAG corpus."
            ) from exc

        return self._corpus_name(corpus)

    def upload_file(
        self,
        file_path: str | Path,
        display_name: str | None = None,
    ) -> UploadResult:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise DocumentImportError(f"File does not exist: {path}")

        rag = self._rag_module
        corpus_name = self.ensure_corpus()
        resolved_display_name = display_name or path.name

        def _do_upload():
            try:
                return rag.upload_file(
                    corpus_name=corpus_name,
                    path=str(path),
                    display_name=resolved_display_name,
                    description="global_corpus",
                    transformation_config=rag.TransformationConfig(
                        chunking_config=rag.ChunkingConfig(
                            chunk_size=self.settings.chunk_size,
                            chunk_overlap=self.settings.chunk_overlap,
                        )
                    ),
                    max_embedding_requests_per_min=self.settings.max_embedding_requests_per_min,
                )
            except TypeError:
                return rag.upload_file(
                    corpus_name=corpus_name,
                    path=str(path),
                    display_name=resolved_display_name,
                    description="global_corpus",
                    transformation_config=rag.TransformationConfig(
                        chunking_config=rag.ChunkingConfig(
                            chunk_size=self.settings.chunk_size,
                            chunk_overlap=self.settings.chunk_overlap,
                        )
                    )
                )

        import time
        import logging
        LOGGER = logging.getLogger("vectorizer")

        operation = None
        last_exc: Exception | None = None
        retry_count = 4
        retry_sleep_seconds = 75

        for attempt in range(1, retry_count + 1):
            try:
                operation = _do_upload()
                break
            except Exception as exc:
                last_exc = exc
                message = str(exc).lower()
                if not any(k in message for k in ('quota', '429', '13', '8', 'internal', 'resource_exhausted')):
                    raise DocumentImportError(
                        f"Unable to upload {path.name} to corpus {corpus_name}."
                    ) from exc
                if attempt == retry_count:
                    raise DocumentImportError(
                        f"Unable to upload {path.name} to corpus {corpus_name} after {retry_count} retries."
                    ) from exc
                LOGGER.warning(
                    'Quota hit for %s; retry %s/%s after %ss',
                    resolved_display_name,
                    attempt,
                    retry_count,
                    retry_sleep_seconds,
                )
                time.sleep(retry_sleep_seconds)

        if operation is None:
            if last_exc is not None:
                raise DocumentImportError(f"Unable to upload {path.name} to corpus {corpus_name}.") from last_exc
            raise DocumentImportError(f"Unable to upload {path.name} to corpus {corpus_name}.")

        return UploadResult(
            corpus_name=corpus_name,
            display_name=resolved_display_name,
            source_path=str(path),
            operation_id=self._extract_operation_name(operation),
            rag_file_id=self._extract_rag_file_id(operation),
        )

    def import_gcs_uris(
        self,
        gcs_uris: list[str],
    ) -> str | None:
        if not gcs_uris:
            raise DocumentImportError("gcs_uris cannot be empty.")

        rag = self._rag_module
        corpus_name = self.ensure_corpus()

        try:
            operation = rag.import_files(
                corpus_name,
                gcs_uris,
                transformation_config=rag.TransformationConfig(
                    chunking_config=rag.ChunkingConfig(
                        chunk_size=self.settings.chunk_size,
                        chunk_overlap=self.settings.chunk_overlap,
                    )
                ),
                max_embedding_requests_per_min=self.settings.max_embedding_requests_per_min,
            )
        except Exception as exc:
            raise DocumentImportError(
                "Unable to import GCS files."
            ) from exc

        return self._extract_operation_name(operation)

    def search_corpus(
        self,
        query: str,
        top_k: int = 5,
        vector_distance_threshold: float | None = None,
    ) -> list[SearchResult]:
        if not query.strip():
            return []

        rag = self._rag_module
        corpus_name = self.ensure_corpus()
        retrieval_filter = None
        if vector_distance_threshold is not None:
            retrieval_filter = rag.Filter(
                vector_distance_threshold=vector_distance_threshold
            )

        try:
            response = rag.retrieval_query(
                rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
                text=query,
                rag_retrieval_config=rag.RagRetrievalConfig(
                    top_k=top_k,
                    filter=retrieval_filter,
                ),
            )
        except Exception as exc:
            raise VectorizerError(
                "Unable to retrieve RAG context."
            ) from exc

        return self._normalize_search_results(response)

    def _find_corpus_by_display_name(self, display_name: str) -> Any | None:
        rag = self._rag_module
        try:
            corpora = rag.list_corpora()
        except Exception as exc:
            raise CorpusProvisionError("Unable to list RAG corpora.") from exc

        for corpus in corpora:
            if getattr(corpus, "display_name", None) == display_name:
                return corpus
        return None

    @staticmethod
    def _corpus_name(corpus: Any) -> str:
        name = getattr(corpus, "name", None)
        if not name:
            raise CorpusProvisionError("Vertex AI returned a corpus without a name.")
        return str(name)

    @staticmethod
    def _extract_operation_name(operation: Any) -> str | None:
        if operation is None:
            return None
        return getattr(operation, "operation", None) or getattr(operation, "name", None)

    @staticmethod
    def _extract_rag_file_id(operation: Any) -> str | None:
        if operation is None:
            return None

        for attr in ("rag_file_id", "rag_file", "resource_name"):
            value = getattr(operation, attr, None)
            if value:
                return str(value)
        return None

    def _normalize_search_results(self, response: Any) -> list[SearchResult]:
        contexts = getattr(response, "contexts", None)
        if contexts is None and isinstance(response, dict):
            contexts = response.get("contexts")
        if not contexts:
            return []

        results: list[SearchResult] = []
        for context in contexts:
            text = self._pick_first_value(context, "text", "chunk_text")
            if not text:
                text = str(context)

            results.append(
                SearchResult(
                    text=text,
                    source_uri=self._pick_first_value(
                        context,
                        "source_uri",
                        "uri",
                        "sourceUri",
                    ),
                    score=self._coerce_float(
                        self._pick_first_value(
                            context,
                            "score",
                            "distance",
                            "vector_distance",
                        )
                    ),
                    raw_chunk=context,
                )
            )
        return results

    @staticmethod
    def _pick_first_value(obj: Any, *keys: str) -> Any | None:
        if isinstance(obj, dict):
            for key in keys:
                if key in obj and obj[key] is not None:
                    return obj[key]
        for key in keys:
            value = getattr(obj, key, None)
            if value is not None:
                return value
        return None

    @staticmethod
    def _coerce_float(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
