from __future__ import annotations

from fastapi import APIRouter

from repo_catalog import (
    get_organizations_data,
    get_people_data,
    get_projects_data,
    get_relationships_data,
    get_skills_data,
)


router = APIRouter(tags=['data'])


@router.get('/organizations')
def list_organizations() -> list[dict[str, str]]:
    return get_organizations_data()


@router.get('/people')
def list_people() -> list[dict[str, str | None]]:
    return get_people_data()


@router.get('/skills')
def list_skills() -> list[dict[str, str | None]]:
    return get_skills_data()


@router.get('/projects')
def list_projects() -> list[dict[str, str | None]]:
    return get_projects_data()


@router.get('/relationships')
def list_relationships() -> list[dict[str, str | None]]:
    return get_relationships_data()
