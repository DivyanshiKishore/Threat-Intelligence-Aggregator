"""
IOC processing pipeline.

Coordinates downloading, parsing,
and validation of threat intelligence feeds.
"""

from pathlib import Path
from typing import List

from normalizer.normalizer import IOCNormalizer
from downloader.downloader import Downloader
from normalizer.schema import IOC
from parsers.parser_manager import ParserManager
from validators.validator import IOCValidator
from utils.logger import get_logger


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
    ) -> None:
        """
        Initialize pipeline.
        """

        self.downloader = downloader
        self.parser_manager = parser_manager
        self.validator = validator
        self.normalizer = normalizer

    def process(
        self,
        url: str,
        filename: str | None = None,
    ) -> List[IOC]:
        """
        Execute the IOC processing pipeline.
        """

        logger.info(
            "Starting pipeline for %s",
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

        iocs = self.parser_manager.parse(feed_path)

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

        logger.info("Normalization completed.")

        return normalized_iocs