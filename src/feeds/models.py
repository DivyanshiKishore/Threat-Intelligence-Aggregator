"""
Models for threat feed management.
"""

from dataclasses import dataclass, field
from urllib.parse import urlparse

from .exceptions import FeedConfigurationError


SUPPORTED_PARSERS = {
    "txt",
    "csv",
    "json",
}


@dataclass
class FeedConfiguration:
    """
    Represents a single threat intelligence feed.

    Attributes:
        name:
            Unique feed identifier.

        url:
            Location of the threat feed.

        parser_type:
            Parser required to process feed data.

        enabled:
            Whether scheduler should process this feed.

        update_interval:
            Feed refresh interval in seconds.

        tags:
            Metadata labels associated with feed.
    """

    name: str
    url: str
    parser_type: str
    filename: str | None = None
    enabled: bool = True
    update_interval: int = 3600
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    def validate(self):
        """
        Validate feed configuration.
        """

        self._validate_name()
        self._validate_url()
        self._validate_parser()
        self._validate_interval()
        self._validate_tags()

    def _validate_name(self):
        if not self.name or not self.name.strip():
            raise FeedConfigurationError(
                "Feed name cannot be empty"
            )

    def _validate_url(self):
        if not self.url or not self.url.strip():
            raise FeedConfigurationError(
                "Feed URL cannot be empty"
            )

        parsed = urlparse(self.url)

        if parsed.scheme not in {"http", "https"}:
            raise FeedConfigurationError(
                "Feed URL must use http or https"
            )

    def _validate_parser(self):
        if self.parser_type not in SUPPORTED_PARSERS:
            raise FeedConfigurationError(
                f"Unsupported parser type: {self.parser_type}"
            )

    def _validate_interval(self):
        if self.update_interval <= 0:
            raise FeedConfigurationError(
                "Update interval must be greater than zero"
            )

    def _validate_tags(self):
        if not isinstance(self.tags, list):
            raise FeedConfigurationError(
                "Tags must be a list"
            )