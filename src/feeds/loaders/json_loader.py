"""
JSON feed configuration loader.
"""

import json

from src.feeds.models import FeedConfiguration
from src.feeds.registry import FeedRegistry
from src.feeds.loaders.base_loader import BaseFeedLoader


class JSONFeedLoader(BaseFeedLoader):
    """
    Loads feeds from JSON configuration files.
    """

    def load(self, path: str) -> FeedRegistry:

        registry = FeedRegistry()

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        feeds = data.get("feeds", [])

        for feed_data in feeds:

            feed = FeedConfiguration(
                name=feed_data["name"],
                url=feed_data["url"],
                parser_type=feed_data["parser_type"],
                enabled=feed_data.get(
                    "enabled",
                    True
                ),
                update_interval=feed_data.get(
                    "update_interval",
                    3600
                ),
                tags=feed_data.get(
                    "tags",
                    []
                )
            )

            registry.add(feed)

        return registry