from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI()


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    active: bool = True


USERS: dict[int, dict[str, Any]] = {
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
    return {"status": "ok"}


@app.get("/api/users/{user_id}")
def get_user(user_id: int) -> dict[str, Any]:
    user = USERS.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@app.post(
    "/api/users",
    status_code=status.HTTP_201_CREATED,
)
def create_user(request: CreateUserRequest) -> dict[str, Any]:
    new_user_id = max(USERS) + 1

    user = {
        "id": new_user_id,
        "name": request.name,
        "active": request.active,
    }

    USERS[new_user_id] = user
    return user