"""Local ingestion pipeline for JSONPlaceholder comments extraction."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.api.client import APIClient
from src.bigquery.loader import BigQueryLoader
from src.config.settings import (
    API_BASE_URL,
    BIGQUERY_RAW_DATASET,
    BIGQUERY_RAW_TABLE,
    DEFAULT_RECORD_LIMIT,
    GCP_PROJECT_ID,
    SOURCE_NAME,
)
from src.utils.logger import get_logger


logger = get_logger(__name__)


def extract_comments(limit: int = DEFAULT_RECORD_LIMIT) -> list[dict[str, Any]]:
    """Extract comments and enrich them with ingestion metadata.

    Args:
        limit: Maximum number of comment records to extract.

    Returns:
        A list of comments enriched with ingestion metadata.
    """
    logger.info("Starting comments extraction.")

    client = APIClient(base_url=API_BASE_URL, logger=logger)
    comments = client.get_comments(limit=limit)

    ingestion_datetime = datetime.now(timezone.utc)
    ingestion_timestamp = ingestion_datetime.isoformat()
    ingestion_date = ingestion_datetime.date().isoformat()

    enriched_comments = [
        {
            **comment,
            "ingestion_timestamp": ingestion_timestamp,
            "ingestion_date": ingestion_date,
            "source": SOURCE_NAME,
        }
        for comment in comments
    ]

    logger.info("Extracted %s comment records.", len(enriched_comments))
    logger.info("Finished comments extraction.")

    return enriched_comments


def run_ingestion_pipeline() -> list[dict[str, Any]]:
    """Run the current local extraction step.

    TODO: Add downstream loading once BigQuery integration is implemented.
    """
    return extract_comments()


def load_comments_to_bigquery(limit: int = DEFAULT_RECORD_LIMIT) -> None:
    """Extract comments and append them to the BigQuery raw table.

    Args:
        limit: Maximum number of comment records to extract and load.
    """
    logger.info("Starting comments load to BigQuery.")

    comments = extract_comments(limit=limit)
    loader = BigQueryLoader(
        project_id=GCP_PROJECT_ID,
        dataset_id=BIGQUERY_RAW_DATASET,
        table_id=BIGQUERY_RAW_TABLE,
        logger=logger,
    )

    loader.create_table_if_not_exists()
    loader.load_records(comments)

    logger.info("Finished comments load to BigQuery.")
