"""
IOC processing pipeline.

Coordinates downloading, parsing,
validation, normalization, and deduplication
of threat intelligence feeds.
"""

from pathlib import Path
from typing import List

from normalizer.normalizer import IOCNormalizer
from downloader.downloader import Downloader
from normalizer.schema import IOC
from parsers.parser_manager import ParserManager
from validators.validator import IOCValidator
from utils.logger import get_logger
from deduplication.deduplicator import IOCDeduplicator


logger = get_logger(__name__)


class PipelineProcessor:
    """
    Main IOC processing workflow.
    """

    def __init__(
        self,
        downloader: Downloader,
        parser_manager: ParserManager,
        validator: IOCValidator,
        normalizer: IOCNormalizer,
        deduplicator: IOCDeduplicator,
    ) -> None:
        """
        Initialize pipeline.
        """

        self.downloader = downloader
        self.parser_manager = parser_manager
        self.validator = validator
        self.normalizer = normalizer
        self.deduplicator = deduplicator

    def process(
        self,
        url: str,
        filename: str | None = None,
     ) -> List[IOC]:
        """
        Process a remote IOC feed.

        Downloads the feed first,
        then executes the processing pipeline.
        """

        logger.info(
            "Starting remote feed pipeline for %s",
            url,
        )

        feed_path = self.downloader.download(
            url,
            filename,
        )

        logger.info(
            "Feed downloaded: %s",
            feed_path,
        )

        return self._process_path(feed_path)

    def process_file(
        self,
        feed_path: Path,
    ) -> List[IOC]:
        """
        Process a local IOC feed file.

        Used for feeds discovered locally.
        """

        logger.info(
            "Starting local feed pipeline for %s",
            feed_path,
        )

        return self._process_path(feed_path)

    def _process_path(
        self,
        feed_path: Path,
    ) -> List[IOC]:
        """
        Execute parsing, validation,
        normalization, and deduplication.
        """

        iocs = self.parser_manager.parse(
            feed_path
        )

        logger.info(
            "Parsed %d IOCs",
            len(iocs),
        )

        valid_iocs = [
            ioc
            for ioc in iocs
            if self.validator.validate(ioc)
        ]

        logger.info(
            "Validation completed. %d valid IOCs",
            len(valid_iocs),
        )

        normalized_iocs = [
            self.normalizer.normalize(ioc)
            for ioc in valid_iocs
        ]

        logger.info(
            "Normalization completed."
        )

        deduplicated_iocs = self.deduplicator.deduplicate(
            normalized_iocs
        )

        logger.info(
            "Deduplication completed. %d unique IOCs",
            len(deduplicated_iocs),
        )

        return deduplicated_iocs