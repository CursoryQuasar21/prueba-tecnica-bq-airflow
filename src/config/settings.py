"""Project settings for the local extraction stage.

TODO: Move environment-specific values to environment variables when needed.
"""

from __future__ import annotations


API_BASE_URL = "https://jsonplaceholder.typicode.com"
API_COMMENTS_ENDPOINT = "/comments"
DEFAULT_RECORD_LIMIT = 100
SOURCE_NAME = "jsonplaceholder_comments"

GCP_PROJECT_ID = "prueba-tecnica-496919"
BIGQUERY_RAW_DATASET = "SANDBOX_prueba_tecnica"
BIGQUERY_RAW_TABLE = "comments_raw"
