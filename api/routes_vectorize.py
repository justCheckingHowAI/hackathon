from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from vectorizer import (
    DocumentImportError,
    VectorizerConfigError,
    VectorizerError,
    VectorizerService,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/vectorize', tags=['vectorize'])

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB


def _get_service() -> VectorizerService:
    return VectorizerService()


@router.post('/{person_id}/upload')
async def upload_and_vectorize(person_id: str, file: UploadFile) -> dict[str, str | None]:
    """Upload a file and vectorize it into the person's RAG corpus."""
    logger.info("Starting upload_and_vectorize for person_id=%s with filename=%s", person_id, file.filename)
    if not file.filename:
        logger.warning("Upload failed: No filename provided for person_id=%s", person_id)
        raise HTTPException(status_code=422, detail='No filename provided.')

    # Read the file content and enforce size limit
    content = await file.read()
    logger.info("Read %d bytes for person_id=%s file=%s", len(content), person_id, file.filename)
    if len(content) > MAX_UPLOAD_SIZE:
        logger.warning(
            "Upload failed: File size %d exceeds limit %d for person_id=%s",
            len(content), MAX_UPLOAD_SIZE, person_id
        )
        raise HTTPException(
            status_code=413,
            detail=f'File exceeds {MAX_UPLOAD_SIZE // (1024 * 1024)} MB limit.',
        )

    # Write to a temp file so VectorizerService can read it from disk
    tmp_dir = Path(tempfile.mkdtemp(prefix='vectorize_'))
    tmp_path = tmp_dir / file.filename
    try:
        tmp_path.write_bytes(content)
        logger.info("Saved temp file to %s, starting vectorization via service", tmp_path)

        service = _get_service()
        result = service.upload_file_for_person(
            person_id=person_id,
            file_path=tmp_path,
            display_name=file.filename,
        )

        logger.info(
            "Successfully vectorized file for person_id=%s. Operation ID: %s, RAG File ID: %s",
            person_id, result.operation_id, result.rag_file_id
        )
        return {
            'person_id': result.person_id,
            'corpus_name': result.corpus_name,
            'display_name': result.display_name,
            'source_path': result.source_path,
            'operation_id': result.operation_id,
            'rag_file_id': result.rag_file_id,
        }
    except VectorizerConfigError as exc:
        logger.error("VectorizerConfigError during upload for person_id=%s: %s", person_id, exc, exc_info=True)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except DocumentImportError as exc:
        logger.error("DocumentImportError during upload for person_id=%s: %s", person_id, exc, exc_info=True)
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except VectorizerError as exc:
        logger.error("VectorizerError during upload for person_id=%s: %s", person_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        logger.info("Cleaning up temp directory %s", tmp_dir)
        shutil.rmtree(tmp_dir, ignore_errors=True)


@router.get('/{person_id}/files')
def list_vectorized_files(person_id: str) -> list[dict[str, str | None]]:
    """List all RAG files in the person's corpus."""
    try:
        service = _get_service()
        corpus_name = service.ensure_person_corpus(person_id)
        rag = service._rag_module

        rag_files = rag.list_files(corpus_name=corpus_name)
        results: list[dict[str, str | None]] = []
        for f in rag_files:
            results.append({
                'name': getattr(f, 'name', None),
                'display_name': getattr(f, 'display_name', None),
                'state': str(getattr(f, 'state', '')),
                'size_bytes': str(getattr(f, 'size_bytes', '')) or None,
                'description': getattr(f, 'description', None),
            })
        return results
    except VectorizerConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except VectorizerError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
