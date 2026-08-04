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


INITIAL_PRODUCTS: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "name": "Barbie's Favorite Food",
        "category": "food",
        "price": 39.99,
        "stock": 15,
        "active": True,
    },
    2: {
        "id": 2,
        "name": "Feefee's Favorite Food",
        "category": "food",
        "price": 34.99,
        "stock": 20,
        "active": True,
    },
    3: {
        "id": 3,
        "name": "Barbie's Cat Teaser Wand",
        "category": "toys",
        "price": 12.99,
        "stock": 8,
        "active": True,
    },
    4: {
        "id": 4,
        "name": "Feefee's Cat Litter",
        "category": "litter",
        "price": 18.50,
        "stock": 0,
        "active": False,
    },
}


USERS: dict[int, dict[str, Any]] = {
    user_id: user.copy()
    for user_id, user in INITIAL_USERS.items()
}


PRODUCTS: dict[int, dict[str, Any]] = {
    product_id: product.copy()
    for product_id, product in INITIAL_PRODUCTS.items()
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


def reset_products() -> None:
    PRODUCTS.clear()

    PRODUCTS.update({
        product_id: product.copy()
        for product_id, product in INITIAL_PRODUCTS.items()
    })