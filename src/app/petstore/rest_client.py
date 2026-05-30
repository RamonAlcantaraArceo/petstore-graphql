"""Async REST client for the Petstore API (mirrors openapi.json operations)."""

from __future__ import annotations

import httpx


class PetstoreClient:
    """Thin async wrapper around the Petstore REST API."""

    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10.0)

    async def aclose(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------ pet --

    async def get_pet_by_id(self, pet_id: int) -> dict:
        resp = await self._client.get(f"/pet/{pet_id}")
        resp.raise_for_status()
        return resp.json()

    async def find_pets_by_status(self, status: str) -> list[dict]:
        resp = await self._client.get("/pet/findByStatus", params={"status": status})
        resp.raise_for_status()
        return resp.json()

    async def find_pets_by_tags(self, tags: list[str]) -> list[dict]:
        resp = await self._client.get("/pet/findByTags", params={"tags": tags})
        resp.raise_for_status()
        return resp.json()

    async def add_pet(self, data: dict) -> dict:
        resp = await self._client.post("/pet", json=data)
        resp.raise_for_status()
        return resp.json()

    async def update_pet(self, data: dict) -> dict:
        resp = await self._client.put("/pet", json=data)
        resp.raise_for_status()
        return resp.json()

    async def delete_pet(self, pet_id: int) -> None:
        resp = await self._client.delete(f"/pet/{pet_id}")
        resp.raise_for_status()

    # --------------------------------------------------------------- store --

    async def get_inventory(self) -> dict[str, int]:
        resp = await self._client.get("/store/inventory")
        resp.raise_for_status()
        return resp.json()

    async def place_order(self, data: dict) -> dict:
        resp = await self._client.post("/store/order", json=data)
        resp.raise_for_status()
        return resp.json()

    async def get_order_by_id(self, order_id: int) -> dict:
        resp = await self._client.get(f"/store/order/{order_id}")
        resp.raise_for_status()
        return resp.json()

    async def delete_order(self, order_id: int) -> None:
        resp = await self._client.delete(f"/store/order/{order_id}")
        resp.raise_for_status()

    # ----------------------------------------------------------------- user --

    async def create_user(self, data: dict) -> dict:
        resp = await self._client.post("/user", json=data)
        resp.raise_for_status()
        return resp.json()

    async def get_user_by_username(self, username: str) -> dict:
        resp = await self._client.get(f"/user/{username}")
        resp.raise_for_status()
        return resp.json()

    async def update_user(self, username: str, data: dict) -> None:
        resp = await self._client.put(f"/user/{username}", json=data)
        resp.raise_for_status()

    async def delete_user(self, username: str) -> None:
        resp = await self._client.delete(f"/user/{username}")
        resp.raise_for_status()

    async def login_user(self, username: str, password: str) -> str:
        resp = await self._client.get(
            "/user/login", params={"username": username, "password": password}
        )
        resp.raise_for_status()
        return resp.text

    async def logout_user(self) -> None:
        resp = await self._client.get("/user/logout")
        resp.raise_for_status()
