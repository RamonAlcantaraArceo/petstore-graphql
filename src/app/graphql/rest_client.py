from __future__ import annotations

from typing import Any

import httpx


class RestError(Exception):
    def __init__(self, status_code: int, detail: Any):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"REST request failed with status {status_code}")


class RestClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._client = httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=timeout)

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        json: Any = None,
        content: bytes | None = None,
    ) -> Any:
        response = await self._client.request(
            method,
            path,
            params=params,
            headers=headers,
            json=json,
            content=content,
        )
        if response.status_code >= 400:
            detail: Any
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise RestError(response.status_code, detail)

        if not response.content:
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        return response.text

    async def get_pet_by_id(self, pet_id: int) -> dict:
        return await self.request("GET", f"/pet/{pet_id}")

    async def find_pets_by_status(self, status: str) -> list[dict]:
        return await self.request("GET", "/pet/findByStatus", params={"status": status})

    async def find_pets_by_tags(self, tags: list[str]) -> list[dict]:
        return await self.request("GET", "/pet/findByTags", params={"tags": tags})

    async def add_pet(self, payload: dict) -> dict:
        return await self.request("POST", "/pet", json=payload)

    async def update_pet(self, payload: dict) -> dict:
        return await self.request("PUT", "/pet", json=payload)

    async def update_pet_with_form(self, pet_id: int, name: str | None, status: str | None) -> Any:
        params = {"name": name, "status": status}
        clean_params = {k: v for k, v in params.items() if v is not None}
        return await self.request("POST", f"/pet/{pet_id}", params=clean_params)

    async def delete_pet(self, pet_id: int, api_key: str | None = None) -> Any:
        headers = {"api_key": api_key} if api_key else None
        return await self.request("DELETE", f"/pet/{pet_id}", headers=headers)

    async def upload_file(
        self,
        pet_id: int,
        additional_metadata: str | None,
        content: bytes | None,
    ) -> dict:
        params = {"additionalMetadata": additional_metadata} if additional_metadata else None
        return await self.request(
            "POST",
            f"/pet/{pet_id}/uploadImage",
            params=params,
            content=content,
        )

    async def get_inventory(self) -> dict[str, int]:
        return await self.request("GET", "/store/inventory")

    async def place_order(self, payload: dict) -> dict:
        return await self.request("POST", "/store/order", json=payload)

    async def get_order_by_id(self, order_id: int) -> dict:
        return await self.request("GET", f"/store/order/{order_id}")

    async def delete_order(self, order_id: int) -> Any:
        return await self.request("DELETE", f"/store/order/{order_id}")

    async def create_user(self, payload: dict) -> Any:
        return await self.request("POST", "/user", json=payload)

    async def create_users_with_list(self, payload: list[dict]) -> Any:
        return await self.request("POST", "/user/createWithList", json=payload)

    async def login_user(self, username: str, password: str) -> str:
        result = await self.request(
            "GET",
            "/user/login",
            params={"username": username, "password": password},
        )
        return str(result)

    async def logout_user(self) -> str:
        result = await self.request("GET", "/user/logout")
        return str(result)

    async def get_user_by_name(self, username: str) -> dict:
        return await self.request("GET", f"/user/{username}")

    async def update_user(self, username: str, payload: dict) -> Any:
        return await self.request("PUT", f"/user/{username}", json=payload)

    async def delete_user(self, username: str) -> Any:
        return await self.request("DELETE", f"/user/{username}")
