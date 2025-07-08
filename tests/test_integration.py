import requests

def test_create_user():
    res = requests.post("http://localhost:5000/users", json={"name": "John"})
    assert res.status_code == 201

def test_get_users():
    res = requests.get("http://localhost:5000/users")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
