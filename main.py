"""
Application entry point.
"""
import argparse
import sys

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
from src.feeds.loaders.yaml_loader import YAMLFeedLoader

from exporter.json_exporter import JSONExporter
from exporter.csv_exporter import CSVExporter

from exporter.correlation_exporter import CorrelationExporter
from exporter.blocklist_exporter import BlocklistExporter
from exporter.report_exporter import ReportExporter

from src.feeds.executor import FeedExecutor
from src.feeds.report import FeedReportGenerator

from normalizer.schema import IOC
from utils.logger import get_logger


logger = get_logger(__name__)

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Threat Intelligence Aggregator"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to feed configuration file",
    )

    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute configured feeds",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run the Threat Intelligence Aggregator.
    """
    
    args = parse_arguments()
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

    correlation_exporter = CorrelationExporter()
    blocklist_exporter = BlocklistExporter()
    report_exporter = ReportExporter()


    if args.run:

        if not args.config:
            logger.error(
                "--config must be supplied when using --run."
            )
            sys.exit(1)

        logger.info(
            "Running configured feed execution."
        )

        loader = YAMLFeedLoader()

        executor = FeedExecutor(
            loader=loader,
            downloader=downloader,
            pipeline_processor=processor,
        )

        try:
            results = executor.execute(args.config)

        except FileNotFoundError:
            logger.error(
                "Configuration file not found: %s",
                args.config,
            )
            sys.exit(1)

        except Exception as error:
            loger.error(
                "Feed execution failed: %s",
            )
            sys.exit(1)


        all_iocs: list[IOC] = []

        for result in results:
            all_iocs.extend(result.iocs)

        all_iocs = deduplicator.deduplicate(all_iocs)
        
        try:
            json_exporter.export(
                all_iocs,
                PathConfig.OUTPUT_DIR / "iocs.json",
           )

            csv_exporter.export(
                all_iocs,
                PathConfig.OUTPUT_DIR / "iocs.csv",
            )

            correlation_exporter.export(
                all_iocs,
                PathConfig.OUTPUT_DIR / "correlation_report.csv",
            )

            blocklist_exporter.export(
                all_iocs,
                PathConfig.OUTPUT_DIR,
            )

            report_exporter.export(
                all_iocs,
                PathConfig.OUTPUT_DIR / "threat_intelligence_report.txt",
            )

        except Exception as error:
            logger.error(
                "IOC export failed: %s",
                error,
            )
            sys.exit(1)


        logger.info(
           "IOC export completed successfully."
        )

        report = FeedReportGenerator().generate(results)
        
        failed_feeds = [
            result
            for result in results
            if not result.success
        ]

        if failed_feeds:
            logger.error(
                "Failed feeds: %d",
                len(failed_feeds),
            )

            for failed_feed in failed_feeds:
                logger.error(
                    "- %s: %s",
                    failed_feed.feed_name,
                    failed_feed.error,
                )

        logger.info("========== Execution Summary ==========")
        logger.info(
            "Total feeds: %d",
            report.total_feeds,
        )
        logger.info(
            "Successful feeds: %d",
            report.successful_feeds,
        )
        logger.info(
            "Total IOCs: %d",
            report.total_iocs,
        )
        logger.info(
            "Execution time: %.2f seconds",
            report.total_execution_time,
        )
        

        sys.exit(0)

          
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
   
    correlation_exporter.export(
        all_iocs,
        PathConfig.OUTPUT_DIR / "correlation_report.csv",
    )

    blocklist_exporter.export(
        all_iocs,
        PathConfig.OUTPUT_DIR,
    )

    report_exporter.export(
        all_iocs,
        PathConfig.OUTPUT_DIR / "threat_intelligence_report.txt"
    )

    logger.info(
        "IOC export completed successfully."
    )


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        logger.exception(
            "Application failed: %s",
            error,
        )
        sys.exit(1)
   