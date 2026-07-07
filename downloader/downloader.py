"""
Downloader module for threat intelligence feeds.
"""

from pathlib import Path
from typing import Optional

import requests

from downloader.exceptions import DownloaderError
from utils.logger import get_logger


logger = get_logger(__name__)


class Downloader:
    """
    Downloads remote threat intelligence feeds
    and stores them locally.
    """

    def __init__(
        self,
        output_dir: Path,
        timeout: int = 10,
        retries: int = 3,
    ) -> None:
        """
        Initialize downloader.

        Args:
            output_dir: Directory where downloaded files are stored.
            timeout: HTTP request timeout in seconds.
            retries: Number of download attempts.
        """

        self.output_dir = output_dir
        self.timeout = timeout
        self.retries = retries

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def download(
        self,
        url: str,
        filename: Optional[str] = None,
    ) -> Path:
        """
        Download a feed from a URL.

        Args:
            url: Remote feed URL.
            filename: Optional output filename.

        Returns:
            Path of downloaded file.

        Raises:
            DownloaderError:
                If download fails.
        """

        if filename is None:
            filename = url.split("/")[-1]

        destination = self.output_dir / filename

        for attempt in range(1, self.retries + 1):

            try:
                logger.info(
                    "Downloading %s (attempt %d/%d)",
                    url,
                    attempt,
                    self.retries,
                )

                response = requests.get(
                    url,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                destination.write_text(
                    response.text,
                    encoding="utf-8",
                )

                logger.info(
                    "Downloaded feed saved to %s",
                    destination,
                )

                return destination

            except requests.RequestException as exc:

                logger.warning(
                    "Download attempt %d failed: %s",
                    attempt,
                    exc,
                )

        logger.error(
            "Failed downloading feed after %d attempts",
            self.retries,
        )

        raise DownloaderError(
            f"Unable to download feed: {url}"
        )