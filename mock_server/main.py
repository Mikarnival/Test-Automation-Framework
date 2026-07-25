from fastapi import FastAPI, HTTPException

app = FastAPI()


USERS = {
    1: {
        "id": 1,
        "name": "Xinrui",
        "active": True,
    },
    2: {
        "id": 2,
        "name": "Mika",
        "active": False,
    },
}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
    }

@app.get("/api/users/{user_id}")
def get_user(user_id: int) -> dict[str, object]:
    user = USERS.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user