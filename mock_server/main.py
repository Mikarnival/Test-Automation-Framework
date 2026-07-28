from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn


app = FastAPI()


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    active: bool = True

class UpdateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    active: bool


USERS: dict[int, dict[str, Any]] = {
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


@app.put(
    "/api/users/{user_id}")
def update_user(user_id: int, request: UpdateUserRequest) -> dict[str, Any]:
    if user_id not in USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_user = {
        "id": user_id,
        "name": request.name,
        "active": request.active,
    }

    USERS[user_id] = update_user
    return update_user


if __name__ == "__main__":
    uvicorn.run(
        "mock_server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
