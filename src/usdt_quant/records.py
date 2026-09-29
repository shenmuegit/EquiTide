from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row


SCHEMA = Path(__file__).resolve().parents[2] / "sql" / "001_initial.sql"


class Records:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def _connect(self) -> psycopg.Connection[Any]:
        return psycopg.connect(self.database_url, row_factory=dict_row)

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(SCHEMA.read_text(encoding="utf-8"))

    def create_backtest(
        self,
        *,
        config: dict[str, Any],
        dependency_versions: dict[str, str],
        data_version: str,
        dataset_dir: Path,
    ) -> dict[str, Any]:
        return self._create_task(
            kind="backtest",
            config=config,
            dependency_versions=dependency_versions,
            data_version=data_version,
            dataset_dir=dataset_dir,
        )

    def create_research(
        self,
        *,
        config: dict[str, Any],
        dependency_versions: dict[str, str],
        data_version: str,
        dataset_dir: Path,
    ) -> dict[str, Any]:
        return self._create_task(
            kind="research",
            config=config,
            dependency_versions=dependency_versions,
            data_version=data_version,
            dataset_dir=dataset_dir,
        )

    def _create_task(
        self,
        *,
        kind: str,
        config: dict[str, Any],
        dependency_versions: dict[str, str],
        data_version: str,
        dataset_dir: Path,
    ) -> dict[str, Any]:
        config_id = str(uuid4())
        task_id = str(uuid4())
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO strategy_configs (id, strategy, config, dependency_versions) VALUES (%s, %s, %s, %s)",
                (config_id, config["baseline"], json.dumps(config), json.dumps(dependency_versions)),
            )
            row = connection.execute(
                """
                INSERT INTO tasks (id, kind, status, strategy_config_id, data_version, dataset_dir)
                VALUES (%s, %s, 'queued', %s, %s, %s)
                RETURNING *
                """,
                (task_id, kind, config_id, data_version, str(dataset_dir)),
            ).fetchone()
            if kind == "research":
                connection.execute(
                    "INSERT INTO experiments (id, kind, parameters) VALUES (%s, %s, %s)",
                    (task_id, kind, json.dumps(config)),
                )
        return dict(row)

    def create_run(self, task_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "INSERT INTO runs (task_id, status) VALUES (%s, 'starting') RETURNING id",
                (task_id,),
            ).fetchone()
        return int(row["id"])

    def mark_running(self, task_id: str, run_id: int, pid: int) -> None:
        with self._connect() as connection:
            connection.execute(
                """UPDATE tasks SET status='running', started_at=coalesce(started_at, now()), error=NULL
                   WHERE id=%s AND status='queued'""",
                (task_id,),
            )
            connection.execute(
                "UPDATE runs SET status='running', pid=%s WHERE id=%s AND status='starting'",
                (pid, run_id),
            )

    def mark_spawned(self, task_id: str, run_id: int, pid: int) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE runs SET pid=%s WHERE id=%s AND task_id=%s AND status='starting'",
                (pid, run_id, task_id),
            )

    def finish(
        self,
        task_id: str,
        run_id: int,
        *,
        result_path: Path | None = None,
        error: str | None = None,
        exit_code: int = 0,
    ) -> bool:
        status = "succeeded" if error is None else "failed"
        with self._connect() as connection:
            run = connection.execute(
                """
                UPDATE runs SET status=%s, exit_code=%s, error=%s, finished_at=now()
                WHERE id=%s AND task_id=%s AND status IN ('starting', 'running')
                RETURNING id
                """,
                (status, exit_code, error, run_id, task_id),
            ).fetchone()
            if run is None:
                return False
            task = connection.execute(
                """
                UPDATE tasks
                SET status=%s, result_path=%s, error=%s, finished_at=now()
                WHERE id=%s AND status IN ('queued', 'running')
                RETURNING kind
                """,
                (status, str(result_path) if result_path else None, error, task_id),
            ).fetchone()
            if task and task["kind"] == "research":
                connection.execute(
                    "UPDATE experiments SET result_path=%s WHERE id=%s",
                    (str(result_path) if result_path else None, task_id),
                )
        return task is not None

    def fail_launch(self, task_id: str, run_id: int, error: str) -> None:
        self.finish(task_id, run_id, error=error, exit_code=-1)

    def active_runs(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT t.id AS task_id, r.id AS run_id, r.pid
                FROM tasks t
                JOIN LATERAL (
                    SELECT id, pid FROM runs
                    WHERE task_id=t.id AND status IN ('starting', 'running')
                    ORDER BY started_at DESC LIMIT 1
                ) r ON true
                WHERE t.status IN ('queued', 'running')
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def fail_queued_without_run(self) -> int:
        with self._connect() as connection:
            rows = connection.execute(
                """
                UPDATE tasks t
                SET status='failed',
                    error='worker was not started before the API stopped',
                    finished_at=now()
                WHERE t.status='queued'
                  AND NOT EXISTS (SELECT 1 FROM runs r WHERE r.task_id=t.id)
                RETURNING t.id
                """
            ).fetchall()
        return len(rows)

    def task(self, task_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT t.*, c.strategy, c.config, c.dependency_versions,
                       r.pid, r.exit_code, r.error AS run_error
                FROM tasks t
                JOIN strategy_configs c ON c.id=t.strategy_config_id
                LEFT JOIN LATERAL (
                    SELECT pid, exit_code, error FROM runs
                    WHERE task_id=t.id ORDER BY started_at DESC LIMIT 1
                ) r ON true
                WHERE t.id=%s
                """,
                (task_id,),
            ).fetchone()
        return dict(row) if row else None

    def tasks(self, limit: int = 50, kind: str | None = None) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT t.*, c.strategy, c.config, c.dependency_versions,
                       r.pid, r.exit_code, r.error AS run_error
                FROM tasks t
                JOIN strategy_configs c ON c.id=t.strategy_config_id
                LEFT JOIN LATERAL (
                    SELECT pid, exit_code, error FROM runs
                    WHERE task_id=t.id ORDER BY started_at DESC LIMIT 1
                ) r ON true
                WHERE (%s::text IS NULL OR t.kind=%s)
                ORDER BY t.created_at DESC LIMIT %s
                """,
                (kind, kind, limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def experiments(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT e.id, e.kind, e.parameters, e.result_path, e.created_at,
                       t.status, t.error, t.data_version, t.started_at, t.finished_at,
                       c.dependency_versions
                FROM experiments e
                JOIN tasks t ON t.id=e.id
                JOIN strategy_configs c ON c.id=t.strategy_config_id
                ORDER BY e.created_at DESC LIMIT %s
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
