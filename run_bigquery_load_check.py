"""Temporary script to validate loading API comments into BigQuery.

TODO: Remove this script once the BigQuery load flow is covered by tests or
Airflow.
"""

from __future__ import annotations

from src.pipelines.ingestion_pipeline import load_comments_to_bigquery


def main() -> None:
    """Run a local BigQuery load check."""
    load_comments_to_bigquery(limit=100)
    print("BigQuery load check completed successfully.")


if __name__ == "__main__":
    main()
