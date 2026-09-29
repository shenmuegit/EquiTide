CREATE TABLE IF NOT EXISTS experiments (
    id text PRIMARY KEY,
    kind text NOT NULL,
    parameters jsonb NOT NULL,
    result_path text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS strategy_configs (
    id text PRIMARY KEY,
    strategy text NOT NULL,
    config jsonb NOT NULL,
    dependency_versions jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tasks (
    id text PRIMARY KEY,
    kind text NOT NULL,
    status text NOT NULL CHECK (status IN ('queued', 'running', 'succeeded', 'failed')),
    strategy_config_id text NOT NULL REFERENCES strategy_configs(id),
    data_version text NOT NULL,
    dataset_dir text NOT NULL,
    result_path text,
    error text,
    created_at timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz,
    finished_at timestamptz
);

CREATE TABLE IF NOT EXISTS runs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    task_id text NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    pid integer,
    status text NOT NULL CHECK (status IN ('starting', 'running', 'succeeded', 'failed')),
    exit_code integer,
    error text,
    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz
);

CREATE INDEX IF NOT EXISTS tasks_created_at_idx ON tasks (created_at DESC);
CREATE INDEX IF NOT EXISTS runs_task_id_idx ON runs (task_id, started_at DESC);
