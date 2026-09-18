from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    document_type TEXT NOT NULL,
    document_key TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    payload TEXT NOT NULL,
    UNIQUE(source, document_type, document_key, observed_at)
);

CREATE TABLE IF NOT EXISTS games (
    game_pk INTEGER PRIMARY KEY,
    game_date TEXT,
    status TEXT,
    away_team_id INTEGER,
    away_team_name TEXT,
    home_team_id INTEGER,
    home_team_name TEXT,
    away_score INTEGER,
    home_score INTEGER,
    venue_id INTEGER,
    first_pitch TEXT,
    source_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS odds_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_event_id TEXT,
    commence_time TEXT,
    home_team TEXT,
    away_team TEXT,
    bookmaker TEXT,
    market TEXT,
    selection TEXT,
    price_american INTEGER,
    point REAL,
    observed_at TEXT NOT NULL,
    source_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS statcast_rows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_pk INTEGER,
    game_date TEXT,
    batter INTEGER,
    pitcher INTEGER,
    batting_team TEXT,
    fielding_team TEXT,
    events TEXT,
    launch_speed REAL,
    launch_angle REAL,
    estimated_woba REAL,
    source_file TEXT
);
"""


class SQLiteStore:
    def __init__(self, path: str):
        self.path = path

        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.connect() as database:
            database.executescript(SCHEMA)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def save_raw(
        self,
        source: str,
        document_type: str,
        document_key: str,
        observed_at: str,
        payload: Any,
    ) -> None:
        query = """
        INSERT OR IGNORE INTO raw_documents (
            source,
            document_type,
            document_key,
            observed_at,
            payload
        )
        VALUES (?, ?, ?, ?, ?)
        """

        with self.connect() as database:
            database.execute(
                query,
                (
                    source,
                    document_type,
                    document_key,
                    observed_at,
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                    ),
                ),
            )
            database.commit()

    def save_game(self, row: tuple) -> None:
        query = """
        INSERT OR REPLACE INTO games (
            game_pk,
            game_date,
            status,
            away_team_id,
            away_team_name,
            home_team_id,
            home_team_name,
            away_score,
            home_score,
            venue_id,
            first_pitch,
            source_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.connect() as database:
            database.execute(query, row)
            database.commit()

    def save_odds(self, rows: list[tuple]) -> None:
        if not rows:
            return

        query = """
        INSERT INTO odds_snapshots (
            external_event_id,
            commence_time,
            home_team,
            away_team,
            bookmaker,
            market,
            selection,
            price_american,
            point,
            observed_at,
            source_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.connect() as database:
            database.executemany(query, rows)
            database.commit()
