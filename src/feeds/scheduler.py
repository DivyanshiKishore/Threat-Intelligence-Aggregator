"""
Feed execution scheduler.

Coordinates feed execution by:
- retrieving enabled feeds
- downloading feeds
- executing IOC pipeline
- collecting execution results
"""

import time
from pathlib import Path

from config import PathConfig
from downloader.feed_downloader import FeedDownloader
from pipeline.processor import PipelineProcessor
from utils.logger import get_logger

from .models import FeedConfiguration
from .registry import FeedRegistry
from .result import FeedExecutionResult


logger = get_logger(__name__)


class FeedScheduler:
    """
    Executes enabled threat intelligence feeds.

    Responsibilities:
    - Orchestrate feed execution
    - Isolate feed failures
    - Measure execution time
    - Return execution results

    Does NOT:
    - Download implementation
    - Parse feeds
    - Validate IOCs
    - Normalize IOCs
    """

    def __init__(
        self,
        registry: FeedRegistry,
        feed_downloader: FeedDownloader,
        pipeline_processor: PipelineProcessor,
    ) -> None:
        self.registry = registry
        self.feed_downloader = feed_downloader
        self.pipeline_processor = pipeline_processor

    def run(self) -> list[FeedExecutionResult]:
        """
        Execute all enabled feeds.

        Returns:
            List of execution results.
        """

        results: list[FeedExecutionResult] = []

        feeds = self.registry.get_enabled_feeds()

        logger.info(
            "Starting scheduler execution for %d feeds",
            len(feeds),
        )

        for feed in feeds:
            result = self._execute_feed(feed)
            results.append(result)

        return results

    def _execute_feed(
        self,
        feed: FeedConfiguration,
    ) -> FeedExecutionResult:
        """
        Execute a single feed safely.
        """

        start_time = time.perf_counter()

        try:
            logger.info(
                "Executing feed: %s",
                feed.name,
            )

            downloaded = self.feed_downloader.download_json_feed(
                feed.name,
                feed.url,
            )

            if not downloaded:
                raise RuntimeError(
                    "Feed download failed"
                )

            feed_path = (
                PathConfig.LOCAL_FEEDS_DIR
                / f"{feed.name}.json"
            )

            iocs = self.pipeline_processor.process_file(
                feed_path
            )

            execution_time = (
                time.perf_counter() - start_time
            )

            logger.info(
                "Feed completed: %s (%d IOCs)",
                feed.name,
                len(iocs),
            )

            return FeedExecutionResult(
                feed_name=feed.name,
                success=True,
                ioc_count=len(iocs),
                execution_time=execution_time,
            )

        except Exception as error:
            execution_time = (
                time.perf_counter() - start_time
            )

            logger.error(
                "Feed failed: %s - %s",
                feed.name,
                error,
            )

            return FeedExecutionResult(
                feed_name=feed.name,
                success=False,
                ioc_count=0,
                execution_time=execution_time,
                error=str(error),
            )