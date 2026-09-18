from __future__ import annotations

from typing import Any

import httpx


class OddsAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def mlb_odds(self) -> list[dict[str, Any]]:
        if not self.api_key:
            return []

        params = {
            "apiKey": self.api_key,
            "regions": "us",
            "markets": (
                "h2h,"
                "spreads,"
                "totals,"
                "team_totals,"
                "h2h_1st_5_innings"
            ),
            "oddsFormat": "american",
        }

        url = f"{self.base_url}/sports/baseball_mlb/odds"

        with httpx.Client(
            timeout=90,
            headers={"User-Agent": "mlb-predictor/1.0"},
        ) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()
