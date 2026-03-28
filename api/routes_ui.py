from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

import psycopg
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db import get_database
from repo_catalog import (
    get_dashboard_counts,
    get_default_organization_id,
    get_organizations_data,
    get_people_data,
    get_projects_data,
    get_relationships_data,
    get_skills_data,
)
from routes_scrapers import validate_repo
from scrape_jobs import list_scrape_jobs
from tasks import scrape_github_repo_task


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

router = APIRouter(tags=['ui'])


def redirect_with_message(
    path: str,
    *,
    success: str | None = None,
    error: str | None = None,
) -> RedirectResponse:
    params: dict[str, str] = {}
    if success:
        params['success'] = success
    if error:
        params['error'] = error

    url = path
    if params:
        url = f'{path}?{urlencode(params)}'

    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


def render_template(
    request: Request,
    template_name: str,
    context: dict[str, object],
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            'request': request,
            'success': request.query_params.get('success'),
            'error': request.query_params.get('error'),
            **context,
        },
    )


def handle_db_error(path: str, action: str, exc: Exception) -> RedirectResponse:
    message = f'Could not {action}. {str(exc).strip() or exc.__class__.__name__}'
    return redirect_with_message(path, error=message)


@router.get('/ui', response_class=HTMLResponse)
def ui_home(request: Request) -> HTMLResponse:
    return render_template(
        request,
        'dashboard.html',
        {'counts': get_dashboard_counts()},
    )


@router.get('/ui/scrapers', response_class=HTMLResponse)
def scrapers_page(request: Request) -> HTMLResponse:
    jobs = list_scrape_jobs(limit=100)
    active_jobs = [job for job in jobs if job['status'] in {'queued', 'running'}]
    completed_jobs = [job for job in jobs if job['status'] == 'completed']
    failed_jobs = [job for job in jobs if job['status'] == 'failed']
    return render_template(
        request,
        'scrapers.html',
        {
            'jobs': jobs,
            'active_jobs_count': len(active_jobs),
            'completed_jobs_count': len(completed_jobs),
            'failed_jobs_count': len(failed_jobs),
        },
    )


@router.post('/ui/scrapers')
async def create_scraper_job(repo: str = Form(...)) -> RedirectResponse:
    try:
        normalized_repo = validate_repo(repo)
    except Exception as exc:
        return handle_db_error('/ui/scrapers', 'queue scraper', exc)

    job = get_database().fetch_one(
        '''
        INSERT INTO scrape_jobs (provider, repo, status, step, message)
        VALUES (%s, %s, 'queued', 'queued', 'Job queued')
        RETURNING id::text
        ''',
        ('github', normalized_repo),
    )
    if job is None or not job.get('id'):
        return redirect_with_message('/ui/scrapers', error='Could not create scraper job.')

    await scrape_github_repo_task.kiq(job['id'], normalized_repo)
    return redirect_with_message('/ui/scrapers', success=f'Scraper queued for {normalized_repo}.')


@router.get('/ui/people', response_class=HTMLResponse)
def people_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    people = get_people_data()
    edit_person = next((person for person in people if person['id'] == edit_id), None)
    return render_template(
        request,
        'people.html',
        {
            'organizations': get_organizations_data(),
            'people': people,
            'edit_person': edit_person,
            'default_organization_id': get_default_organization_id(),
        },
    )


@router.post('/ui/people')
def create_person(
    organization_id: str = Form(...),
    external_key: str = Form(...),
    full_name: str = Form(...),
    display_name: str = Form(default=''),
    role_title: str = Form(default=''),
    seniority: str = Form(default=''),
    department: str = Form(default=''),
    bio: str = Form(default=''),
    github_login: str = Form(default=''),
    clone_status: str = Form(default='pending'),
    status_value: str = Form(default='active', alias='status'),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            '''
            INSERT INTO people (
                organization_id,
                external_key,
                full_name,
                display_name,
                role_title,
                seniority,
                department,
                bio,
                github_login,
                clone_status,
                status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                organization_id,
                external_key.strip(),
                full_name.strip(),
                display_name.strip() or None,
                role_title.strip() or None,
                seniority.strip() or None,
                department.strip() or None,
                bio.strip() or None,
                github_login.strip() or None,
                clone_status.strip() or 'pending',
                status_value.strip() or 'active',
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error('/ui/people', 'create person', exc)

    return redirect_with_message('/ui/people', success='Person created.')


@router.post('/ui/people/{person_id}/update')
def update_person(
    person_id: str,
    organization_id: str = Form(...),
    external_key: str = Form(...),
    full_name: str = Form(...),
    display_name: str = Form(default=''),
    role_title: str = Form(default=''),
    seniority: str = Form(default=''),
    department: str = Form(default=''),
    bio: str = Form(default=''),
    github_login: str = Form(default=''),
    clone_status: str = Form(default='pending'),
    status_value: str = Form(default='active', alias='status'),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            '''
            UPDATE people
            SET organization_id = %s,
                external_key = %s,
                full_name = %s,
                display_name = %s,
                role_title = %s,
                seniority = %s,
                department = %s,
                bio = %s,
                github_login = %s,
                clone_status = %s,
                status = %s,
                updated_at = NOW()
            WHERE id = %s
            ''',
            (
                organization_id,
                external_key.strip(),
                full_name.strip(),
                display_name.strip() or None,
                role_title.strip() or None,
                seniority.strip() or None,
                department.strip() or None,
                bio.strip() or None,
                github_login.strip() or None,
                clone_status.strip() or 'pending',
                status_value.strip() or 'active',
                person_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(f'/ui/people?edit_id={person_id}', 'update person', exc)

    return redirect_with_message('/ui/people', success='Person updated.')


@router.post('/ui/people/{person_id}/delete')
def delete_person(person_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute('DELETE FROM people WHERE id = %s', (person_id,))
    except psycopg.Error as exc:
        return handle_db_error('/ui/people', 'delete person', exc)

    return redirect_with_message('/ui/people', success='Person deleted.')


@router.get('/ui/skills', response_class=HTMLResponse)
def skills_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    skills = get_skills_data()
    edit_skill = next((skill for skill in skills if skill['id'] == edit_id), None)
    return render_template(
        request,
        'skills.html',
        {
            'organizations': get_organizations_data(),
            'skills': skills,
            'edit_skill': edit_skill,
            'default_organization_id': get_default_organization_id(),
        },
    )


@router.post('/ui/skills')
def create_skill(
    organization_id: str = Form(...),
    canonical_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(default=''),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            'INSERT INTO skills (organization_id, canonical_name, category, description) VALUES (%s, %s, %s, %s)',
            (
                organization_id,
                canonical_name.strip(),
                category.strip(),
                description.strip() or None,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error('/ui/skills', 'create skill', exc)

    return redirect_with_message('/ui/skills', success='Skill created.')


@router.post('/ui/skills/{skill_id}/update')
def update_skill(
    skill_id: str,
    organization_id: str = Form(...),
    canonical_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(default=''),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            '''
            UPDATE skills
            SET organization_id = %s,
                canonical_name = %s,
                category = %s,
                description = %s
            WHERE id = %s
            ''',
            (
                organization_id,
                canonical_name.strip(),
                category.strip(),
                description.strip() or None,
                skill_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(f'/ui/skills?edit_id={skill_id}', 'update skill', exc)

    return redirect_with_message('/ui/skills', success='Skill updated.')


@router.post('/ui/skills/{skill_id}/delete')
def delete_skill(skill_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute('DELETE FROM skills WHERE id = %s', (skill_id,))
    except psycopg.Error as exc:
        return handle_db_error('/ui/skills', 'delete skill', exc)

    return redirect_with_message('/ui/skills', success='Skill deleted.')


@router.get('/ui/projects', response_class=HTMLResponse)
def projects_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    projects = get_projects_data()
    edit_project = next((project for project in projects if project['id'] == edit_id), None)
    return render_template(
        request,
        'projects.html',
        {
            'organizations': get_organizations_data(),
            'projects': projects,
            'edit_project': edit_project,
            'default_organization_id': get_default_organization_id(),
        },
    )


@router.post('/ui/projects')
def create_project(
    organization_id: str = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(default=''),
    status_value: str = Form(default='active', alias='status'),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            'INSERT INTO projects (organization_id, name, slug, description, status) VALUES (%s, %s, %s, %s, %s)',
            (
                organization_id,
                name.strip(),
                slug.strip(),
                description.strip() or None,
                status_value.strip() or 'active',
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error('/ui/projects', 'create project', exc)

    return redirect_with_message('/ui/projects', success='Project created.')


@router.post('/ui/projects/{project_id}/update')
def update_project(
    project_id: str,
    organization_id: str = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(default=''),
    status_value: str = Form(default='active', alias='status'),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            '''
            UPDATE projects
            SET organization_id = %s,
                name = %s,
                slug = %s,
                description = %s,
                status = %s
            WHERE id = %s
            ''',
            (
                organization_id,
                name.strip(),
                slug.strip(),
                description.strip() or None,
                status_value.strip() or 'active',
                project_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(f'/ui/projects?edit_id={project_id}', 'update project', exc)

    return redirect_with_message('/ui/projects', success='Project updated.')


@router.post('/ui/projects/{project_id}/delete')
def delete_project(project_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute('DELETE FROM projects WHERE id = %s', (project_id,))
    except psycopg.Error as exc:
        return handle_db_error('/ui/projects', 'delete project', exc)

    return redirect_with_message('/ui/projects', success='Project deleted.')


@router.get('/ui/relationships', response_class=HTMLResponse)
def relationships_page(request: Request, edit_id: str | None = None) -> HTMLResponse:
    relationships = get_relationships_data()
    edit_relationship = next(
        (relationship for relationship in relationships if relationship['id'] == edit_id),
        None,
    )
    return render_template(
        request,
        'relationships.html',
        {
            'organizations': get_organizations_data(),
            'people': get_people_data(),
            'relationships': relationships,
            'edit_relationship': edit_relationship,
            'default_organization_id': get_default_organization_id(),
            'relationship_types': [
                'manager_of',
                'mentor_of',
                'reviewer_of',
                'collaborates_with',
                'depends_on',
                'backup_for',
                'knowledge_source_for',
            ],
        },
    )


@router.post('/ui/relationships')
def create_relationship(
    organization_id: str = Form(...),
    from_person_id: str = Form(...),
    to_person_id: str = Form(...),
    relationship_type: str = Form(...),
    strength: str = Form(default=''),
    confidence: str = Form(default='1'),
    source: str = Form(default=''),
    notes: str = Form(default=''),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            '''
            INSERT INTO people_relationships (
                organization_id,
                from_person_id,
                to_person_id,
                relationship_type,
                strength,
                confidence,
                source,
                notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                organization_id,
                from_person_id,
                to_person_id,
                relationship_type.strip(),
                strength.strip() or None,
                confidence.strip() or '1',
                source.strip() or None,
                notes.strip() or None,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error('/ui/relationships', 'create relationship', exc)

    return redirect_with_message('/ui/relationships', success='Relationship created.')


@router.post('/ui/relationships/{relationship_id}/update')
def update_relationship(
    relationship_id: str,
    organization_id: str = Form(...),
    from_person_id: str = Form(...),
    to_person_id: str = Form(...),
    relationship_type: str = Form(...),
    strength: str = Form(default=''),
    confidence: str = Form(default='1'),
    source: str = Form(default=''),
    notes: str = Form(default=''),
) -> RedirectResponse:
    db = get_database()
    try:
        db.execute(
            '''
            UPDATE people_relationships
            SET organization_id = %s,
                from_person_id = %s,
                to_person_id = %s,
                relationship_type = %s,
                strength = %s,
                confidence = %s,
                source = %s,
                notes = %s
            WHERE id = %s
            ''',
            (
                organization_id,
                from_person_id,
                to_person_id,
                relationship_type.strip(),
                strength.strip() or None,
                confidence.strip() or '1',
                source.strip() or None,
                notes.strip() or None,
                relationship_id,
            ),
        )
    except psycopg.Error as exc:
        return handle_db_error(
            f'/ui/relationships?edit_id={relationship_id}',
            'update relationship',
            exc,
        )

    return redirect_with_message('/ui/relationships', success='Relationship updated.')


@router.post('/ui/relationships/{relationship_id}/delete')
def delete_relationship(relationship_id: str) -> RedirectResponse:
    db = get_database()
    try:
        db.execute('DELETE FROM people_relationships WHERE id = %s', (relationship_id,))
    except psycopg.Error as exc:
        return handle_db_error('/ui/relationships', 'delete relationship', exc)

    return redirect_with_message('/ui/relationships', success='Relationship deleted.')
