#!/usr/bin/env python3
"""
Simple helper to wait for a Postgres database to become available using psycopg2.
Reads DATABASE_URL environment variable (supports SQLAlchemy-style URLs like
postgresql+psycopg2://user:pass@host:port/dbname and plain postgresql://...)
"""
import os
import time
import sys
from urllib.parse import urlparse

import psycopg2
from psycopg2 import OperationalError


def parse_database_url(url: str):
    # Normalize SQLAlchemy URL with +psycopg2
    if url.startswith("postgresql+psycopg2://"):
        url = url.replace("postgresql+psycopg2://", "postgresql://", 1)
    parsed = urlparse(url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "dbname": parsed.path.lstrip("/") or None,
    }


def wait_for_postgres(database_url: str, timeout: int = 60):
    cfg = parse_database_url(database_url)
    start = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                host=cfg["host"],
                port=cfg["port"],
                user=cfg["user"],
                password=cfg["password"],
                dbname=cfg["dbname"],
                connect_timeout=3,
            )
            conn.close()
            print("Postgres is available at %s:%s" % (cfg["host"], cfg["port"]))
            return 0
        except OperationalError as e:
            elapsed = time.time() - start
            if elapsed > timeout:
                print(f"Timed out waiting for Postgres after {timeout} seconds: {e}")
                return 1
            print('.', end='', flush=True)
            time.sleep(1)


if __name__ == '__main__':
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        print('DATABASE_URL not set; assuming Postgres on localhost:5432')
        DATABASE_URL = 'postgresql://sgi:sgi_pass@localhost:5432/sgi_db'
    rc = wait_for_postgres(DATABASE_URL, timeout=int(os.environ.get('DB_WAIT_TIMEOUT', 60)))
    sys.exit(rc)
