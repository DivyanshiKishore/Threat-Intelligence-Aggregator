"""
Base interface for feed configuration loaders.
"""

from abc import ABC, abstractmethod

from src.feeds.registry import FeedRegistry


class BaseFeedLoader(ABC):
    """
    Abstract feed loader.

    Every configuration loader must implement load().
    """

    @abstractmethod
    def load(self, path: str) -> FeedRegistry:
        """
        Load feed configurations.

        Args:
            path:
                Configuration file path.

        Returns:
            FeedRegistry containing feeds.
        """

        pass