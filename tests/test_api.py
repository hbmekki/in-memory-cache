
import pytest
from time import sleep
from api import create_app


@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

@pytest.fixture
def oldest_first_client():
    app = create_app('testing-oldest-first')
    with app.test_client() as client:
        yield client

@pytest.fixture
def newest_first_client():
    app = create_app('testing-newest-first')
    with app.test_client() as client:
        yield client

def set_entry(client, key, obj, ttl = None):
    path = f"/object/{key}"
    if ttl:
        path += f"?ttl={ttl}"
    return client.post(path, json=obj)

def test_set(client):
    rv = set_entry(client, 'key_a', {"data": "Hello"})
    assert rv.status_code == 200
    assert rv.get_json()["message"] == "success"

    rv = client.get("/object/key_a")
    assert rv.get_json() == {"data": "Hello"}

def test_update(client):
    set_entry(client, 'key_a', {"data": "Hello"})

    rv = client.put("/object/key_a", json={"data": "Howdy!"})
    assert rv.status_code == 200
    assert rv.get_json() == {"message": "success"}

    rv = client.get("/object/key_a")
    assert rv.status_code == 200
    assert rv.get_json() == {"data": "Howdy!"}

def test_get_no_key_set(client):
    rv = client.get("/object/key_a")
    assert rv.status_code == 404
    assert rv.get_json()["message"] == "Object at key_a is not found or expired"

def test_get_with_key_set(client):
    set_entry(client, 'key_a', {"data": [1, 2]})
    rv = client.get("/object/key_a")
    assert rv.status_code == 200
    assert rv.get_json() == {"data": [1, 2]}

def test_delete_no_key_set(client):
    rv = client.delete("/object/key_a")
    assert rv.status_code == 404
    assert rv.get_json() == {"message": "Object at key_a is not found or expired"}

def test_delete_with_key_set(client):
    set_entry(client, 'key_a', {"data": "Hi"})
    rv = client.delete("/object/key_a")
    assert rv.status_code == 200
    assert rv.get_json() == {"message": "success"}

def test_expiry(client):
    set_entry(client, 'key_a', {"data": "key_a"}, ttl=5)
    sleep(5)
    rv = client.get("/object/key_a")
    assert rv.status_code == 404
    assert rv.get_json()["message"] == "Object at key_a is not found or expired"

def test_reject_policy(client):
    set_entry(client, 'key_a', {"data": "key_a"})
    set_entry(client, 'key_b', {"data": "key_b"})
    rv = set_entry(client, 'key_c', {"data": "key_c"})
    assert rv.status_code == 507
    assert rv.get_json() == {"message": "The server has no storage"}

def test_newest_first_policy(newest_first_client):
    client = newest_first_client

    set_entry(client, 'key_a', {"data": "key_a"}, ttl=0)
    set_entry(client, 'key_b', {"data": "key_b"}, ttl=0)

    # this should replace the key_b
    set_entry(client, 'key_c', {"data": "key_c"}, ttl=0)

    rv = client.get('/object/key_c')
    assert rv.status_code == 200

    rv = client.get('/object/key_b')
    assert rv.status_code == 404

def test_newest_first_policy(oldest_first_client):
    client = oldest_first_client
    set_entry(client, 'key_a', {"data": "key_a"}, ttl=0)
    set_entry(client, 'key_b', {"data": "key_b"}, ttl=0)

    # this should replace the key_a
    set_entry(client, 'key_c', {"data": "key_c"}, ttl=0)

    rv = client.get('/object/key_c')
    assert rv.status_code == 200

    rv = client.get('/object/key_a')
    assert rv.status_code == 404