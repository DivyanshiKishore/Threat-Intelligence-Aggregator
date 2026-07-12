"""
Feed execution integration.

Coordinates:
- loading feed configurations
- creating scheduler
- executing enabled feeds
"""

from downloader.downloader import Downloader
from pipeline.processor import PipelineProcessor
from utils.logger import get_logger

from .loaders.base_loader import BaseFeedLoader
from .registry import FeedRegistry
from .result import FeedExecutionResult
from .scheduler import FeedScheduler


logger = get_logger(__name__)


class FeedExecutor:
    """
    High-level feed execution coordinator.

    Responsibilities:
    - Load feed configuration
    - Create scheduler
    - Execute scheduler

    Does NOT:
    - Download feeds
    - Parse feeds
    - Validate IOCs
    - Normalize IOCs
    """

    def __init__(
        self,
        loader: BaseFeedLoader,
        downloader: Downloader,
        pipeline_processor: PipelineProcessor,
    ) -> None:
        self.loader = loader
        self.downloader = downloader
        self.pipeline_processor = pipeline_processor

    def execute(
        self,
        config_path: str,
    ) -> list[FeedExecutionResult]:
        """
        Load configuration and execute all enabled feeds.

        Args:
            config_path:
                Path to YAML or JSON configuration.

        Returns:
            List of FeedExecutionResult objects.
        """

        logger.info(
            "Loading feed configuration from %s",
            config_path,
        )

        registry: FeedRegistry = self.loader.load(config_path)

        logger.info(
            "Loaded %d feed(s)",
            registry.count(),
        )

        scheduler = FeedScheduler(
            registry=registry,
            downloader=self.downloader,
            pipeline_processor=self.pipeline_processor,
        )

        logger.info("Starting feed execution")

        results = scheduler.run()

        logger.info(
            "Feed execution completed"
        )

        return results