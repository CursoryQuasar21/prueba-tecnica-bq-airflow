"""Temporary script to validate local API extraction.

TODO: Remove this script once the extraction flow is covered by tests or Airflow.
"""

from __future__ import annotations

from pprint import pprint

from src.pipelines.ingestion_pipeline import extract_comments


def main() -> None:
    """Run a local extraction check and print a small sample."""
    records = extract_comments(limit=100)

    print(f"Total records: {len(records)}")

    if not records:
        print("No records extracted.")
        return

    print("First record:")
    pprint(records[0])

    print("First record keys:")
    pprint(list(records[0].keys()))


if __name__ == "__main__":
    main()
