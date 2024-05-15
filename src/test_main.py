from fastapi.testclient import TestClient

import ast
from uuid import uuid4
from src.main import app

client = TestClient(app)


# def test_read_users():
#     response = client.get("/api/v1/all_users")
#     assert response.status_code == 200
#     assert isinstance(type(response.content), type(bytes))


def test_create_user():
    new_user_json = {
        "id": str(uuid4()),
        "first_name": "Name1",
        "last_name": "Lastname1",
        "gender": "male",
        "roles": ["admin"],
    }
    response_new_user = client.post("/api/v1/users", json=new_user_json)
    dict_new_id = ast.literal_eval(response_new_user.content.decode())
    assert dict_new_id.get("id")
    new_id = dict_new_id.get("id")
    url_verify_user = f"/api/v1/user/{new_id}"
    response_get_user = client.get(url_verify_user)
    assert response_get_user.status_code == 200


def test_delete_users():
    response = client.get("/api/v1/all_users")
    content_users = ast.literal_eval(response.content.decode())
    assert content_users[0]

    # Get the first user
    user_to_delete = content_users[0]

    # Needed data to verify
    id = user_to_delete["id"]
    url_delete = f"/api/v1/users/{id}"
    url_verify = f"/api/v1/user/{id}"

    # Delete user
    response_delete = client.delete(url_delete)
    assert response_delete.status_code == 200

    # Verify the user was deleted
    verify_delete = client.get(url_verify)
    assert verify_delete.status_code != 200
