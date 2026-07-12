"""
Feed execution scheduler.

Coordinates feed execution by:
- retrieving enabled feeds
- downloading feeds
- executing IOC pipeline
- collecting execution results
"""

import time

from downloader.downloader import Downloader
from pipeline.processor import PipelineProcessor
from utils.logger import get_logger

from .models import FeedConfiguration
from .registry import FeedRegistry
from .result import FeedExecutionResult
from .history_manager import FeedHistoryManager


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
        downloader: Downloader,
        pipeline_processor: PipelineProcessor,
        history_manager: FeedHistoryManager | None = None,
    ) -> None:
        self.registry = registry
        self.downloader = downloader
        self.pipeline_processor = pipeline_processor
        self.history_manager = (
            history_manager
            if history_manager is not None
            else FeedHistoryManager()
        )

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

        iocs = []

        try:
            logger.info(
                "Executing feed: %s",
                feed.name,
            )

            iocs = self.pipeline_processor.process(
                feed.url,
                filename=feed.filename,
            )

            execution_time = (
                time.perf_counter() - start_time
            )

            logger.info(
                "Feed completed: %s (%d IOCs)",
                feed.name,
                len(iocs),
            )

            result = FeedExecutionResult(
                feed_name=feed.name,
                success=True,
                ioc_count=len(iocs),
                execution_time=execution_time,
                iocs=iocs,
            )
            
            self.history_manager.update(result)

            return result

        except Exception as error:
            execution_time = (
                time.perf_counter() - start_time
            )

            logger.error(
                "Feed failed: %s - %s",
                feed.name,
                error,
            )

            result = FeedExecutionResult(
                feed_name=feed.name,
                success=False,
                ioc_count=0,
                execution_time=execution_time,
                error=str(error),
                iocs=iocs,
            )

            self.history_manager.update(result)

            return result