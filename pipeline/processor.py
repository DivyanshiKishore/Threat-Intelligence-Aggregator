"""
IOC processing pipeline.

Coordinates downloading, parsing,
and validation of threat intelligence feeds.
"""

from pathlib import Path
from typing import List

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
    ) -> None:
        """
        Initialize pipeline.

        Args:
            downloader: Feed downloader instance.
            parser_manager: Parser selection engine.
            validator: IOC validation engine.
        """

        self.downloader = downloader
        self.parser_manager = parser_manager
        self.validator = validator

    def process(
        self,
        url: str,
        filename: str | None = None,
    ) -> List[IOC]:
        """
        Execute complete IOC processing pipeline.

        Args:
            url: Threat feed URL.
            filename: Optional local filename.

        Returns:
            List of validated IOC objects.
        """

        logger.info(
            "Starting pipeline for %s",
            url,
        )

        # Step 1: Download feed
        feed_path: Path = self.downloader.download(
            url,
            filename,
        )

        logger.info(
            "Feed downloaded: %s",
            feed_path,
        )

        # Step 2: Parse feed
        iocs = self.parser_manager.parse(
            feed_path
        )

        logger.info(
            "Parsed %d IOCs",
            len(iocs),
        )

        # Step 3: Validate IOCs
        valid_iocs = [
            ioc
            for ioc in iocs
            if self.validator.validate(ioc)
        ]

        logger.info(
            "Validation completed. %d valid IOCs",
            len(valid_iocs),
        )

        return valid_iocs