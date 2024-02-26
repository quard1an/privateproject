from starlette.testclient import TestClient
import pytest
from app.main import app, group_set


@pytest.fixture(scope="module")
def get_client():
    client = TestClient(app)
    yield client


def test_healtcheck(get_client):
    good_response = get_client.get("/")
    assert good_response.status_code == 200


def test_create_group(get_client):
    good_response = get_client.post('/v1/group/', json={"groupId": "1"})
    assert good_response.status_code == 201
    bad_response = get_client.post('/v1/group/', json={"groupId": "1"})
    assert bad_response.status_code == 400


def test_delete_group(get_client):
    group_set.add("1")
    good_response = get_client.request("DELETE", '/v1/group/', json={"groupId": "1"})
    assert good_response.status_code == 200
    bad_response = get_client.request("DELETE", '/v1/group/', json={"groupId": "1"})
    assert bad_response.status_code == 400


def test_get_groups(get_client):
    group_set.add("1")
    good_response = get_client.get('/v1/group/1')
    assert good_response.status_code == 200
    bad_response = get_client.get('/v1/group/2')
    assert bad_response.status_code == 404
