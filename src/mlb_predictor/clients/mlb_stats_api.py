from __future__ import annotations

from typing import Any

import httpx


class MLBStatsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        with httpx.Client(
            timeout=90,
            headers={"User-Agent": "mlb-predictor/1.0"},
        ) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def schedule(self, game_date: str) -> dict[str, Any]:
        return self.get(
            "schedule",
            {
                "sportId": 1,
                "date": game_date,
                "hydrate": "team,probablePitcher,venue",
            },
        )

    def live_feed(self, game_pk: int) -> dict[str, Any]:
        return self.get(f"game/{game_pk}/feed/live")

    def boxscore(self, game_pk: int) -> dict[str, Any]:
        return self.get(f"game/{game_pk}/boxscore")

    def linescore(self, game_pk: int) -> dict[str, Any]:
        return self.get(f"game/{game_pk}/linescore")
