"""
Application entry point.
"""

from config import NetworkConfig, PathConfig
from downloader.downloader import Downloader
from normalizer.normalizer import IOCNormalizer
from parsers.parser_manager import ParserManager
from pipeline.processor import PipelineProcessor
from utils.logger import get_logger
from validators.validator import IOCValidator


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

    processor = PipelineProcessor(
        downloader=downloader,
        parser_manager=parser_manager,
        validator=validator,
        normalizer=normalizer,
    )

    logger.info(
        "Threat Intelligence Aggregator started."
    )

    logger.info(
        "Pipeline initialized successfully."
    )

    # Feed processing will be connected
    # after the deduplication engine is implemented.


if __name__ == "__main__":
    main()