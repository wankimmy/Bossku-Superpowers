"""HTTP handlers."""
from router import route

USERS = [{"id": "1", "name": "Aisyah"}, {"id": "2", "name": "Wei Jie"}, {"id": "3", "name": "Ravi"}]
PREFIX = "/api/v2"


def find_user(user_id):
    for user in USERS:
        if user["id"] == user_id:
            return user
    raise KeyError(user_id)


@route("GET", PREFIX + "/users")
def list_users():
    return USERS


@route("GET", PREFIX + "/users/names")
def list_user_names():
    return [u["name"] for u in USERS]


@route("GET", PREFIX + "/users/{id}")
def get_user(user_id):
    return find_user(user_id)
