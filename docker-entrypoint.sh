#!/bin/bash
set -e
alembic upgrade head
uvicorn password_manager.main:app --reload --host 0.0.0.0 --port 80