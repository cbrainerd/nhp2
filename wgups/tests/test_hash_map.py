import pytest

from wgups.hash_map import HashMap

@pytest.fixture
def hashmap():
    return populate_hashmap(HashMap())



@pytest.fixture
def collision_hashmap():
    return HashMap(size=1)


def populate_hashmap(empty_hashmap):
    empty_hashmap[1] = "one"
    empty_hashmap[2] = "two"
    empty_hashmap[3] = "three"
    return empty_hashmap


def test_empty():
    assert not any([x for x in HashMap()._buckets])

def test_setitem(hashmap):
    hashmap["foo"] = "bar"
    assert any([x for x in hashmap._buckets])

def test_getitem(hashmap):
    hashmap["foo"] = "bar"
    assert hashmap["foo"] == "bar"

def get_getitem_raises(hashmap):
    with pytest.raises(KeyError):
        hashmap["this key doesn't exist"]

def test_replace_item(hashmap):
    hashmap["foo"] = "bar"
    hashmap["foo"] = "baz"
    assert hashmap["foo"] == "baz"

def test_collision():
    hashmap = HashMap(size=1)
    populate_hashmap(hashmap)

    assert len(hashmap._bucket(1)) == 3
    assert hashmap[1] == "one"
    assert hashmap[2] == "two"
    assert hashmap[3] == "three"


def test_collision_replace():
    hashmap = HashMap(size=1)
    populate_hashmap(hashmap)
    hashmap[2] = "updated"

    assert len(hashmap._bucket(1)) == 3
    assert hashmap[1] == "one"
    assert hashmap[2] == "updated"
    assert hashmap[3] == "three"

def test_delitem(hashmap):
    assert 2 in hashmap
    del hashmap[2]
    assert 2 not in hashmap

def test_pop(hashmap):
    assert hashmap.pop(2) == "two"
    assert 2 not in hashmap

def test_stress(hashmap):
    for i in range(2000):
        hashmap[i] = str(i)

    for i in range(2000):
        assert hashmap[i] == str(i)

    for i in range(2000):
        assert i in hashmap

    keys = hashmap.keys()
    assert len(keys) == 2000
    for i in range(2000):
        assert i in keys
    
    assert -1 not in hashmap
    assert 2000 not in hashmap

    for i in range(2000):
        del hashmap[i]
    
    for i in range(2000):
        assert i not in hashmap
