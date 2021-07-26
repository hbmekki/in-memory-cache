import json
from time import sleep
from .main import EvictionStrategies, Cache

def test_contructor():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    assert cache.max_slots == 2
    assert cache.default_ttl == 5

def test_contructor_negative_params():
    cache = Cache(-1, -1, EvictionStrategies.REJECT);
    assert cache.max_slots == 10000
    assert cache.default_ttl == 3600

def test_set_entry():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.set_entry('key_a', json.dumps({"data": "hello"}))
    assert rv == True
    rv = cache.get_entry('key_a')
    assert rv.json_str == json.dumps({"data": "hello"})

def test_update_entry():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    cache.set_entry('key_a', json.dumps({"data": "hello"}))
    rv = cache.set_entry('key_a', json.dumps({"data": "Howdy!"}))
    assert rv == True
    rv = cache.get_entry('key_a')
    assert rv.json_str == json.dumps({"data": "Howdy!"})

def test_get_entry_with_no_key_set():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.get_entry('key_a')
    assert rv == None

def test_get_entry_with_key_set():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.set_entry('key_a', json.dumps({"data": "hello"}))
    assert rv == True
    rv = cache.get_entry('key_a')
    assert rv.json_str == json.dumps({"data": "hello"})

def test_get_entry_after_expiry():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.set_entry('key_a', json.dumps({"data": "hello"}), 2)
    assert rv == True
    sleep(2)
    rv = cache.get_entry('key_a')
    assert rv == None

def test_delete_entry_with_no_key_set():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.delete_entry('key_a')
    assert rv == False

def test_delete_entry_with_key_set():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.set_entry('key_a', json.dumps({"data": "hello"}))
    assert rv == True
    rv = cache.delete_entry('key_a')
    assert rv == True

def test_delete_entry_after_expiry():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    rv = cache.set_entry('key_a', json.dumps({"data": "hello"}), 2)
    assert rv == True
    sleep(2)
    rv = cache.delete_entry('key_a')
    assert rv == False

def test_reject_policy():
    cache = Cache(2, 5, EvictionStrategies.REJECT);
    cache.set_entry('key_a', json.dumps({"data": "key_a"}), ttl=0)
    cache.set_entry('key_b', json.dumps({"data": "key_b"}), ttl=0)
    rv = cache.set_entry('key_c', json.dumps({"data": "key_c"}), ttl=0)
    assert rv == False

def test_newest_first_policy():
    cache = Cache(2, 5, EvictionStrategies.NEWEST_FIRST);
    cache.set_entry('key_a', json.dumps({"data": "key_a"}), ttl=0)
    cache.set_entry('key_b', json.dumps({"data": "key_b"}), ttl=0)
    cache.set_entry('key_c', json.dumps({"data": "key_c"}), ttl=0)

    rv = cache.get_entry('key_c')
    assert rv.json_str == json.dumps({"data": "key_c"})
    rv = cache.get_entry('key_b')
    assert rv == None

def test_oldest_first_policy():
    cache = Cache(2, 5, EvictionStrategies.OLDEST_FIRST);
    cache.set_entry('key_a', json.dumps({"data": "key_a"}), ttl=0)
    cache.set_entry('key_b', json.dumps({"data": "key_b"}), ttl=0)
    cache.set_entry('key_c', json.dumps({"data": "key_c"}), ttl=0)

    rv = cache.get_entry('key_c')
    assert rv.json_str == json.dumps({"data": "key_c"})
    rv = cache.get_entry('key_a')
    assert rv == None