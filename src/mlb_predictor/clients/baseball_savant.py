from __future__ import annotations

from datetime import date
from io import StringIO

import httpx
import pandas as pd


class BaseballSavant:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def statcast(
        self,
        start_date: date,
        end_date: date,
        team: str = "",
    ) -> pd.DataFrame:
        params = {
            "all": "true",
            "type": "details",
            "player_type": "batter",
            "game_date_gt": start_date.isoformat(),
            "game_date_lt": end_date.isoformat(),
            "team": team,
        }

        url = f"{self.base_url}/statcast_search/csv"

        with httpx.Client(
            timeout=180,
            headers={"User-Agent": "mlb-predictor/1.0"},
        ) as client:
            response = client.get(url, params=params)
            response.raise_for_status()

        return pd.read_csv(
            StringIO(response.text),
            low_memory=False,
        )
