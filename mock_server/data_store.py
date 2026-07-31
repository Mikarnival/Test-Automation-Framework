from typing import Any


INITIAL_USERS: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "name": "Barbie",
        "active": True,
    },
    2: {
        "id": 2,
        "name": "Feefee",
        "active": False,
    },
}

USERS: dict[int, dict[str, Any]] = {
    user_id: user.copy()
    for user_id, user in INITIAL_USERS.items()
}

def reset_users() -> None:
    """
    Reset the USERS dictionary to its initial state.
    """
    USERS.clear()

    USERS.update({
        user_id: user.copy()
        for user_id, user in INITIAL_USERS.items()
    })