#!/bin/sh
set -eu

source_env_path="${SUPERSET_ROOT_PATH}/.env"
target_env_path="${SUPERSET_WORKSPACE_PATH}/.env"

if [ ! -f "$source_env_path" ]; then
  printf 'Missing source env: %s\n' "$source_env_path" >&2
  exit 1
fi

cp -f "$source_env_path" "$target_env_path"
printf 'Copied %s -> %s\n' "$source_env_path" "$target_env_path"
