import json
import requests

from config import NetworkConfig, PathConfig
from utils.logger import get_logger

logger = get_logger("Downloader")


class FeedDownloader:
    """Downloads and stores threat intelligence feeds."""

    def __init__(self):
        PathConfig.LOCAL_FEEDS_DIR.mkdir(parents=True, exist_ok=True)

    def download_json_feed(self, name: str, url: str) -> bool:
        """
        Download a JSON feed and save it locally.

        Args:
            name: Name of the feed.
            url: Feed URL.

        Returns:
            True if successful, otherwise False.
        """

        try:
            logger.info(f"Downloading '{name}'...")

            response = requests.get(
                url,
                timeout=NetworkConfig.REQUEST_TIMEOUT,
                headers={
                    "User-Agent": NetworkConfig.USER_AGENT
                }
            )

            response.raise_for_status()

            data = response.json()

            file_path = PathConfig.LOCAL_FEEDS_DIR / f"{name}.json"

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            logger.info(f"Saved '{name}' to {file_path}")

            return True

        except requests.RequestException as error:
            logger.error(f"Failed to download '{name}': {error}")
            return False

        except ValueError:
            logger.error(f"'{name}' did not return valid JSON.")
            return False