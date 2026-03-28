from __future__ import annotations

import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_LOCATION = 'us-east4'
DEFAULT_EMBEDDING_MODEL = 'publishers/google/models/text-embedding-005'
DEFAULT_CORPUS_DISPLAY_NAME = 'gemelius corpus'
SKIP_DIR_NAMES = {'scripts', '__pycache__'}


@dataclass(slots=True)
class Settings:
    project_id: str
    location: str
    embedding_model: str
    corpus_display_name: str
    source_dir: Path
    chunk_size: int
    chunk_overlap: int
    max_embedding_requests_per_min: int

    @classmethod
    def from_env(cls) -> 'Settings':
        project_id = os.getenv('GCP_PROJECT_ID') or os.getenv('GOOGLE_CLOUD_PROJECT')
        if not project_id:
            raise ValueError('Missing GCP project id. Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT.')

        source_dir = Path(
            os.getenv(
                'VERTEX_RAG_SOURCE_DIR',
                Path(__file__).resolve().parent / 'mike-data',
            )
        ).resolve()

        return cls(
            project_id=project_id,
            location=os.getenv('GCP_LOCATION', DEFAULT_LOCATION),
            embedding_model=os.getenv('VERTEX_RAG_EMBEDDING_MODEL', DEFAULT_EMBEDDING_MODEL),
            corpus_display_name=os.getenv('VERTEX_RAG_CORPUS_NAME', DEFAULT_CORPUS_DISPLAY_NAME),
            source_dir=source_dir,
            chunk_size=int(os.getenv('VERTEX_RAG_CHUNK_SIZE', '512')),
            chunk_overlap=int(os.getenv('VERTEX_RAG_CHUNK_OVERLAP', '100')),
            max_embedding_requests_per_min=int(os.getenv('VERTEX_RAG_EMBEDDING_RPM', '1000')),
        )


def build_stage_file(source_path: Path, source_dir: Path, stage_dir: Path) -> Path:
    relative_path = source_path.relative_to(source_dir)
    stage_path = stage_dir / relative_path.with_suffix(relative_path.suffix + '.txt')
    stage_path.parent.mkdir(parents=True, exist_ok=True)

    if source_path.suffix.lower() == '.json':
        payload = json.loads(source_path.read_text(encoding='utf-8'))
        body = json.dumps(payload, indent=2, ensure_ascii=False)
    else:
        body = source_path.read_text(encoding='utf-8')

    header = f'Original path: {relative_path.as_posix()}\n\n'
    stage_path.write_text(header + body, encoding='utf-8')
    return stage_path


def iter_source_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(source_dir.rglob('*')):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(source_dir).parts):
            continue
        files.append(path)
    return files


def init_rag(settings: Settings):
    try:
        import vertexai
        from vertexai import rag
    except ImportError as exc:
        raise RuntimeError(
            'vertexai is not installed. Install api/requirements.txt first.'
        ) from exc

    vertexai.init(project=settings.project_id, location=settings.location)
    return rag


def ensure_corpus(rag, settings: Settings) -> str:
    for corpus in rag.list_corpora():
        if getattr(corpus, 'display_name', None) == settings.corpus_display_name:
            name = getattr(corpus, 'name', None)
            if not name:
                raise RuntimeError('Vertex AI returned a corpus without a name.')
            return str(name)

    corpus = rag.create_corpus(
        display_name=settings.corpus_display_name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=rag.RagEmbeddingModelConfig(
                vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                    publisher_model=settings.embedding_model
                )
            )
        ),
    )
    name = getattr(corpus, 'name', None)
    if not name:
        raise RuntimeError('Vertex AI returned a corpus without a name.')
    return str(name)


def existing_display_names(rag, corpus_name: str) -> set[str]:
    return {
        str(display_name)
        for rag_file in rag.list_files(corpus_name=corpus_name)
        for display_name in [getattr(rag_file, 'display_name', None)]
        if display_name
    }


def upload_file(rag, settings: Settings, corpus_name: str, stage_path: Path, display_name: str):
    try:
        return rag.upload_file(
            corpus_name=corpus_name,
            path=str(stage_path),
            display_name=display_name,
            description=f'source_dir={settings.source_dir}',
            transformation_config=rag.TransformationConfig(
                chunking_config=rag.ChunkingConfig(
                    chunk_size=settings.chunk_size,
                    chunk_overlap=settings.chunk_overlap,
                )
            ),
            max_embedding_requests_per_min=settings.max_embedding_requests_per_min,
        )
    except TypeError:
        return rag.upload_file(
            corpus_name=corpus_name,
            path=str(stage_path),
            display_name=display_name,
            description=f'source_dir={settings.source_dir}',
        )


def main() -> int:
    settings = Settings.from_env()
    if not settings.source_dir.exists() or not settings.source_dir.is_dir():
        raise FileNotFoundError(f'Source directory does not exist: {settings.source_dir}')

    source_files = iter_source_files(settings.source_dir)
    if not source_files:
        print(f'No source files found in {settings.source_dir}')
        return 0

    rag = init_rag(settings)
    corpus_name = ensure_corpus(rag, settings)
    already_uploaded = existing_display_names(rag, corpus_name)

    stage_dir = Path(tempfile.mkdtemp(prefix='vertex_rag_stage_'))
    uploaded_count = 0
    skipped_count = 0

    try:
        for source_path in source_files:
            relative_name = source_path.relative_to(settings.source_dir).as_posix()
            if relative_name in already_uploaded:
                skipped_count += 1
                print(f'Skip existing: {relative_name}')
                continue

            stage_path = build_stage_file(source_path, settings.source_dir, stage_dir)
            operation = upload_file(rag, settings, corpus_name, stage_path, relative_name)
            uploaded_count += 1
            print(
                'Uploaded:',
                relative_name,
                'operation=',
                getattr(operation, 'operation', None) or getattr(operation, 'name', None),
            )
    finally:
        shutil.rmtree(stage_dir, ignore_errors=True)

    print('')
    print(f'Corpus: {settings.corpus_display_name}')
    print(f'Corpus resource: {corpus_name}')
    print(f'Source directory: {settings.source_dir}')
    print(f'Uploaded files: {uploaded_count}')
    print(f'Skipped existing files: {skipped_count}')
    print(f'Total discovered files: {len(source_files)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
