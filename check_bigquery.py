"""Temporary BigQuery connectivity check.

TODO: Remove this script once local BigQuery connectivity has been validated.
"""

from __future__ import annotations

from google.cloud import bigquery


PROJECT_ID = "prueba-tecnica-496919"


def main() -> None:
    """Validate local connectivity to BigQuery and list available datasets."""
    try:
        client = bigquery.Client(project=PROJECT_ID)

        print(f"Active project: {client.project}")
        print("Available datasets:")

        datasets = list(client.list_datasets(project=PROJECT_ID))

        if not datasets:
            print("- No datasets found.")
            return

        for dataset in datasets:
            print(f"- {dataset.dataset_id}")

    except Exception as exc:
        print(f"BigQuery connectivity check failed: {exc}")


if __name__ == "__main__":
    main()
