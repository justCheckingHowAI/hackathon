from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path

from schemas_hiring_packs import HiringPack


PERSON_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
DEFAULT_HIRING_PACKS_DIR = Path(__file__).resolve().parent.parent / 'data' / 'hiring-packs'


class HiringPackStorageError(RuntimeError):
    """Raised when hiring pack storage cannot be read or written safely."""


class HiringPacksStore:
    def __init__(self, base_dir: Path | None = None) -> None:
        configured_dir = os.getenv('HIRING_PACKS_DIR')
        if base_dir is not None:
            self.base_dir = Path(base_dir)
        elif configured_dir:
            self.base_dir = Path(configured_dir)
        else:
            self.base_dir = DEFAULT_HIRING_PACKS_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def load(self, person_id: str) -> HiringPack | None:
        path = self._path_for_person(person_id)
        if not path.exists():
            return None

        try:
            payload = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            raise HiringPackStorageError(f'Could not read hiring pack for {person_id}.') from exc

        try:
            return HiringPack.model_validate(payload)
        except Exception as exc:
            raise HiringPackStorageError(f'Could not validate hiring pack for {person_id}.') from exc

    def save(self, person_id: str, hiring_pack: HiringPack) -> HiringPack:
        path = self._path_for_person(person_id)
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                'w',
                dir=path.parent,
                prefix=f'{path.stem}.',
                suffix='.tmp',
                delete=False,
                encoding='utf-8',
            ) as tmp_file:
                json.dump(hiring_pack.model_dump(mode='json'), tmp_file, indent=2, ensure_ascii=False)
                tmp_file.write('\n')
                temp_path = Path(tmp_file.name)

            temp_path.replace(path)
        except OSError as exc:
            raise HiringPackStorageError(f'Could not save hiring pack for {person_id}.') from exc
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink(missing_ok=True)

        return hiring_pack

    def _path_for_person(self, person_id: str) -> Path:
        if not PERSON_ID_PATTERN.fullmatch(person_id):
            raise HiringPackStorageError('person_id may contain only letters, numbers, underscores, and hyphens.')
        return self.base_dir / f'{person_id}.json'


def get_hiring_packs_store() -> HiringPacksStore:
    return HiringPacksStore()
