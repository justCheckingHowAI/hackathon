import json

from fastapi.testclient import TestClient

from hiring_packs_store import HiringPacksStore
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


def test_put_hiring_pack_persists_file(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    payload = build_hiring_pack_payload()

    response = client.put('/hiring-packs/mike', json=payload)

    assert response.status_code == 200
    assert response.json() == payload
    assert json.loads((tmp_path / 'mike.json').read_text()) == payload


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


def test_put_hiring_pack_rejects_invalid_payload(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    payload = build_hiring_pack_payload()
    del payload['recommendedRole']

    response = client.put('/hiring-packs/mike', json=payload)

    assert response.status_code == 422


def test_put_hiring_pack_rejects_person_id_mismatch(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    payload = build_hiring_pack_payload()
    payload['person']['id'] = 'someone-else'

    response = client.put('/hiring-packs/mike', json=payload)

    assert response.status_code == 400
    assert response.json() == {
        'detail': 'person.id must match the person_id path parameter.'
    }


def test_get_hiring_pack_returns_500_for_corrupted_file(tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    app.dependency_overrides = {get_hiring_packs_store: lambda: store}
    client = TestClient(app)
    (tmp_path / 'mike.json').write_text('{not-valid-json', encoding='utf-8')

    response = client.get('/hiring-packs/mike')

    assert response.status_code == 500
    assert response.json() == {'detail': 'Could not read hiring pack for mike.'}
