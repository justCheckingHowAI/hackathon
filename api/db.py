from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row


class DatabaseConfigError(RuntimeError):
    """Raised when database configuration is missing."""


@dataclass(slots=True)
class DatabaseSettings:
    database_url: str

    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise DatabaseConfigError("Missing DATABASE_URL environment variable.")
        return cls(database_url=database_url)


class Database:
    def __init__(self, settings: DatabaseSettings | None = None) -> None:
        self.settings = settings or DatabaseSettings.from_env()

    @contextmanager
    def connection(self) -> Iterator[psycopg.Connection[Any]]:
        with psycopg.connect(self.settings.database_url, row_factory=dict_row) as conn:
            yield conn

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                row = cur.fetchone()
        return dict(row) if row else None

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
        return [dict(row) for row in rows]

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> None:
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
            conn.commit()

    def execute_returning(
        self,
        query: str,
        params: tuple[Any, ...] = (),
    ) -> dict[str, Any] | None:
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                row = cur.fetchone()
            conn.commit()
        return dict(row) if row else None

    def ping(self) -> None:
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")


def get_database() -> Database:
    return Database()
