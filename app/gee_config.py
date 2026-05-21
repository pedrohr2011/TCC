# -*- coding: utf-8 -*-
import os
from pathlib import Path

import ee


PROJECT_ENV_VAR = "GEE_PROJECT_ID"
BASE_DIR = Path(__file__).resolve().parent.parent


def _load_local_env():
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_gee_project_id():
    _load_local_env()
    return os.getenv(PROJECT_ENV_VAR)


def initialize_gee():
    project_id = get_gee_project_id()
    if not project_id:
        raise RuntimeError(
            "Projeto do Google Earth Engine nao configurado.\n"
            f"Defina a variavel {PROJECT_ENV_VAR} com o ID do seu projeto Google Cloud/GEE.\n"
            "Exemplo em .env:\n"
            f"{PROJECT_ENV_VAR}=seu-projeto-gee"
        )

    try:
        ee.Initialize(project=project_id)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=project_id)

    return project_id
