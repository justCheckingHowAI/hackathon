from __future__ import annotations

import argparse
from pathlib import Path

from service_vapi import VapiClient, get_settings
from vapi_sync import pull_assistant_config, push_assistant_config


DEFAULT_CONFIG_PATH = Path('config/vapi/assistant.json')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Sync the managed Vapi assistant with repo config.')
    parser.add_argument('command', choices=['pull', 'push'])
    parser.add_argument(
        '--config',
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f'Path to assistant config JSON (default: {DEFAULT_CONFIG_PATH})',
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = get_settings()

    if not settings.private_key:
        raise SystemExit('Missing VAPI_PRIVATE_KEY environment variable.')
    if not settings.assistant_id:
        raise SystemExit('Missing VAPI_ASSISTANT_ID environment variable.')

    client = VapiClient(settings)
    if args.command == 'pull':
        pull_assistant_config(
            client=client,
            assistant_id=settings.assistant_id,
            output_path=args.config,
        )
        print(f'Pulled assistant {settings.assistant_id} to {args.config}')
        return 0

    push_assistant_config(
        client=client,
        assistant_id=settings.assistant_id,
        input_path=args.config,
    )
    print(f'Pushed assistant config from {args.config} to {settings.assistant_id}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
