import json
from pathlib import Path

from fastapi.testclient import TestClient

from hiring_packs_store import (
    DEMO_HIRING_PACK_FILENAME,
    DEMO_HIRING_PACK_TARGET_PERSON_ID,
    HiringPacksStore,
)
from main import app
from routes_hiring_packs import get_hiring_packs_store
from schemas_hiring_packs import HiringPack


def build_hiring_pack_payload() -> dict:
    return {
        'person': {
            'id': 'mike',
            'name': 'Mike Grabowski',
            'role': 'Senior React Native Engineer & OSS Lead',
            'avatar': 'MG',
            'department': 'Engineering',
            'yearsAtCompany': 6,
            'keyProjects': ['React Native CLI', 'Re.Pack'],
        },
        'skills': [
            {
                'name': 'Build Systems & Tooling',
                'level': 'expert',
                'evidence': ['Created Re.Pack and maintained its runtime plugins.'],
                'category': 'Technical',
            }
        ],
        'gapSummary': 'The team loses its primary owner of bundler internals and OSS coordination.',
        'recommendedRole': {
            'title': 'Staff React Native Platform Engineer',
            'description': 'Own build tooling and native module architecture.',
            'seniority': 'Staff / Principal',
        },
        'scorecard': [
            {
                'criterion': 'Build tooling & bundler expertise',
                'weight': 0.3,
                'description': 'Can debug Metro or Webpack internals.',
            }
        ],
        'interviewQuestions': [
            {
                'question': 'How would you debug a broken chunk loading flow in React Native?',
                'category': 'Build Tooling',
            }
        ],
        'mustHave': ['Deep React Native platform experience'],
        'niceToHave': ['Hermes internals experience'],
        'redFlags': ['No native mobile experience'],
    }


def setup_function() -> None:
    app.dependency_overrides = {}


def write_demo_hiring_pack(base_dir: Path, payload: dict) -> None:
    (base_dir / DEMO_HIRING_PACK_FILENAME).write_text(
        json.dumps(payload),
        encoding='utf-8',
    )


def test_put_hiring_pack_persists_file(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    demo_payload = build_hiring_pack_payload()
    write_demo_hiring_pack(tmp_path, demo_payload)

    response = client.put(
        '/hiring-packs/any-person',
        json={'ignored': True, 'person': {'id': 'someone-else'}},
    )

    assert response.status_code == 200
    assert response.json() == demo_payload
    assert json.loads((tmp_path / f'{DEMO_HIRING_PACK_TARGET_PERSON_ID}.json').read_text()) == demo_payload


def test_get_hiring_pack_returns_saved_payload(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    payload = build_hiring_pack_payload()
    store.save('mike', HiringPack.model_validate(payload))

    response = client.get('/hiring-packs/mike')

    assert response.status_code == 200
    assert response.json() == payload


def test_get_hiring_pack_returns_404_when_missing(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)

    response = client.get('/hiring-packs/missing-person')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Hiring pack not found.'}


def test_put_hiring_pack_accepts_any_payload_and_ignores_it(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    demo_payload = build_hiring_pack_payload()
    write_demo_hiring_pack(tmp_path, demo_payload)

    response = client.put('/hiring-packs/mike', json={'foo': 'bar'})

    assert response.status_code == 200
    assert response.json() == demo_payload


def test_put_hiring_pack_returns_500_when_demo_file_is_missing(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)

    response = client.put('/hiring-packs/mike', json={'anything': 'goes'})

    assert response.status_code == 500
    assert response.json() == {
        'detail': f'Could not find demo hiring pack: {DEMO_HIRING_PACK_FILENAME}.'
    }


def test_get_hiring_pack_returns_500_for_corrupted_file(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    (tmp_path / 'mike.json').write_text('{not-valid-json', encoding='utf-8')

    response = client.get('/hiring-packs/mike')

    assert response.status_code == 500
    assert response.json() == {'detail': 'Could not read hiring pack for mike.'}
