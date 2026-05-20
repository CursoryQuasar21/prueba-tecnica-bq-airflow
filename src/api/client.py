"""REST API client for JSONPlaceholder comments extraction."""

from __future__ import annotations

import logging
from typing import Any

import requests

from src.config.settings import API_COMMENTS_ENDPOINT
from src.utils.logger import get_logger


class APIClient:
    """Client for extracting data from a REST API."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create an API client.

        Args:
            base_url: Base URL for the API.
            timeout: Request timeout in seconds.
            logger: Optional logger instance.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logger or get_logger(__name__)
        self.session = requests.Session()

    def get_comments(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Fetch comments from the API.

        Args:
            limit: Optional maximum number of records to return.

        Returns:
            A list of comment records.

        Raises:
            requests.RequestException: If the HTTP request fails.
            TypeError: If the API response is not a list.
        """
        url = f"{self.base_url}{API_COMMENTS_ENDPOINT}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException:
            self.logger.exception("Failed to fetch comments from API.")
            raise

        data = response.json()

        if not isinstance(data, list):
            self.logger.error("Unexpected API response type: %s", type(data).__name__)
            raise TypeError("Expected API response to be a list.")

        if limit is not None:
            return data[:limit]

        return data
