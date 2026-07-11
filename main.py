"""
Application entry point.
"""

from pathlib import Path
from typing import List

from config import (
    NetworkConfig,
    PathConfig,
    FeedConfig,
)

from downloader.downloader import Downloader
from normalizer.normalizer import IOCNormalizer
from parsers.parser_manager import ParserManager
from pipeline.processor import PipelineProcessor
from validators.validator import IOCValidator
from deduplication.deduplicator import IOCDeduplicator

from exporter.json_exporter import JSONExporter
from exporter.csv_exporter import CSVExporter

from normalizer.schema import IOC
from utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    """
    Run the Threat Intelligence Aggregator.
    """

    downloader = Downloader(
        output_dir=PathConfig.LOCAL_FEEDS_DIR,
        timeout=NetworkConfig.REQUEST_TIMEOUT,
        retries=NetworkConfig.MAX_RETRIES,
    )

    parser_manager = ParserManager()

    validator = IOCValidator()

    normalizer = IOCNormalizer()

    deduplicator = IOCDeduplicator()

    processor = PipelineProcessor(
        downloader=downloader,
        parser_manager=parser_manager,
        validator=validator,
        normalizer=normalizer,
        deduplicator=deduplicator,
    )

    json_exporter = JSONExporter()

    csv_exporter = CSVExporter()


    logger.info(
        "Threat Intelligence Aggregator started."
    )


    all_iocs: List[IOC] = []


    for feed in FeedConfig.FEEDS:

        try:
            logger.info(
                "Processing feed: %s",
                feed["name"],
            )

            if feed["type"] == "url":

                iocs = processor.process(
                    feed["location"],
                    feed.get("filename"),
                )

            elif feed["type"] == "file":

                iocs = processor.process_file(
                    Path(feed["location"])
                )

            else:
                logger.warning(
                    "Unknown feed type: %s",
                    feed["type"],
                )
                continue


            all_iocs.extend(iocs)


        except Exception as error:

            logger.error(
                "Failed processing %s: %s",
                feed["name"],
                error,
            )


    logger.info(
        "Total collected IOCs: %d",
        len(all_iocs),
    )


    # Final cross-feed deduplication
    all_iocs = deduplicator.deduplicate(
        all_iocs
    )


    logger.info(
        "Final unique IOCs: %d",
        len(all_iocs),
    )


    json_exporter.export(
        all_iocs,
        PathConfig.OUTPUT_DIR / "iocs.json",
    )


    csv_exporter.export(
        all_iocs,
        PathConfig.OUTPUT_DIR / "iocs.csv",
    )


    logger.info(
        "IOC export completed successfully."
    )


if __name__ == "__main__":
    main()