from __future__ import annotations

import json
import os
import time
from copy import deepcopy
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


class ProductRepository:
    """Small Supabase REST adapter with a safe local catalog fallback."""

    def __init__(self, cache_seconds: int = 60) -> None:
        self.url = (
            os.getenv("SUPABASE_URL")
            or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
            or ""
        ).rstrip("/")
        self.key = (
            os.getenv("SUPABASE_PUBLISHABLE_KEY")
            or os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")
            or ""
        )
        self.cache_seconds = cache_seconds
        self._cache: list[dict] = []
        self._cached_at = 0.0
        self.last_source = "not-loaded"

    @property
    def is_configured(self) -> bool:
        parsed_url = urlparse(self.url)
        return bool(
            self.key
            and parsed_url.scheme in {"http", "https"}
            and parsed_url.netloc
        )

    def list_products(self, fallback: list[dict]) -> list[dict]:
        now = time.monotonic()
        if self._cache and now - self._cached_at < self.cache_seconds:
            self.last_source = "supabase-cache"
            return deepcopy(self._cache)

        if not self.is_configured:
            self.last_source = "local-fallback"
            return deepcopy(fallback)

        try:
            query = urlencode({"select": "*", "order": "sort_order.asc"})
            request = Request(
                f"{self.url}/rest/v1/products?{query}",
                headers={
                    "apikey": self.key,
                    "Authorization": f"Bearer {self.key}",
                    "Accept": "application/json",
                },
            )
            with urlopen(request, timeout=4) as response:
                rows = json.loads(response.read().decode("utf-8"))
            if not isinstance(rows, list):
                raise ValueError("Supabase products response must be a list")
            products = [self._normalize(row) for row in rows]
        except (HTTPError, URLError, TimeoutError, ValueError, TypeError, KeyError, OSError):
            self.last_source = "local-fallback"
            return deepcopy(fallback)

        if not products:
            self.last_source = "local-fallback"
            return deepcopy(fallback)

        self._cache = products
        self._cached_at = now
        self.last_source = "supabase"
        return deepcopy(products)

    @staticmethod
    def _normalize(row: dict) -> dict:
        price = float(row.get("price", 0.01))
        return {
            "id": str(row["sku"]),
            "sku": str(row["sku"]),
            "name": row["name"],
            "category": row["category"],
            "category_label": row["category_label"],
            "weight": row["weight"],
            "case": row["case_size"],
            "image": row["image"],
            "source_url": row["source_url"],
            "status": row["status"],
            "price": price,
            "price_label": f"${price:.2f}",
            "sort_order": int(row["sort_order"]),
            "is_available": bool(row.get("is_available", True)),
        }
