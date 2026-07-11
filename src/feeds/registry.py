"""
Feed registry management.

Responsible for storing and managing
threat intelligence feed configurations.
"""

from typing import Dict, List

from .models import FeedConfiguration
from .exceptions import FeedRegistryError


class FeedRegistry:
    """
    Registry for threat intelligence feeds.

    Responsibilities:
    - Store feed configurations
    - Retrieve feeds
    - Filter enabled feeds
    - Remove feeds

    Does NOT:
    - Download feeds
    - Parse feeds
    - Execute pipeline
    """

    def __init__(self):
        self._feeds: Dict[str, FeedConfiguration] = {}

    def add(self, feed: FeedConfiguration) -> None:
        """
        Add a feed configuration.

        Raises:
            FeedRegistryError:
                If feed already exists.
        """

        if feed.name in self._feeds:
            raise FeedRegistryError(
                f"Feed already exists: {feed.name}"
            )

        self._feeds[feed.name] = feed

    def remove(self, feed_name: str) -> None:
        """
        Remove feed configuration.
        """

        if feed_name not in self._feeds:
            raise FeedRegistryError(
                f"Feed not found: {feed_name}"
            )

        del self._feeds[feed_name]

    def get(self, feed_name: str) -> FeedConfiguration:
        """
        Retrieve feed by name.
        """

        if feed_name not in self._feeds:
            raise FeedRegistryError(
                f"Feed not found: {feed_name}"
            )

        return self._feeds[feed_name]

    def get_all(self) -> List[FeedConfiguration]:
        """
        Return all registered feeds.
        """

        return list(self._feeds.values())

    def get_enabled_feeds(self) -> List[FeedConfiguration]:
        """
        Return only enabled feeds.
        """

        return [
            feed
            for feed in self._feeds.values()
            if feed.enabled
        ]

    def count(self) -> int:
        """
        Return total number of feeds.
        """

        return len(self._feeds)