"""BigQuery loading utilities for raw ingestion data."""

from __future__ import annotations

import logging
from typing import Any

from google.api_core.exceptions import NotFound
from google.cloud import bigquery

from src.utils.logger import get_logger


COMMENTS_RAW_SCHEMA = [
    bigquery.SchemaField("postId", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("id", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("email", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("body", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ingestion_timestamp", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("ingestion_date", "DATE", mode="NULLABLE"),
    bigquery.SchemaField("source", "STRING", mode="NULLABLE"),
]


class BigQueryLoader:
    """Load records into a BigQuery raw table."""

    def __init__(
        self,
        project_id: str,
        dataset_id: str,
        table_id: str,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create a BigQuery loader.

        Args:
            project_id: Google Cloud project identifier.
            dataset_id: BigQuery dataset identifier.
            table_id: BigQuery table identifier.
            logger: Optional logger instance.
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.logger = logger or get_logger(__name__)
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.{table_id}"

    def create_table_if_not_exists(self) -> None:
        """Create the raw BigQuery table when it does not exist."""
        try:
            self.client.get_table(self.table_ref)
            self.logger.info("BigQuery table already exists: %s", self.table_ref)
        except NotFound:
            self.logger.info("Creating BigQuery table: %s", self.table_ref)
            table = bigquery.Table(self.table_ref, schema=COMMENTS_RAW_SCHEMA)
            self.client.create_table(table)
            self.logger.info("BigQuery table created: %s", self.table_ref)
        except Exception:
            self.logger.exception("Failed to verify or create table: %s", self.table_ref)
            raise

    def load_records(self, records: list[dict[str, Any]]) -> None:
        """Append records to the configured BigQuery table.

        Args:
            records: Records to append to the raw table.
        """
        if not records:
            self.logger.warning("No records provided for BigQuery load.")
            return

        self.logger.info(
            "Starting BigQuery load of %s records into %s.",
            len(records),
            self.table_ref,
        )

        job_config = bigquery.LoadJobConfig(
            schema=COMMENTS_RAW_SCHEMA,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        try:
            load_job = self.client.load_table_from_json(
                records,
                self.table_ref,
                job_config=job_config,
            )
            load_job.result()

            self.logger.info(
                "Finished BigQuery load into %s. Loaded rows: %s.",
                self.table_ref,
                len(records),
            )
        except Exception:
            self.logger.exception("Failed to load records into BigQuery.")
            raise
