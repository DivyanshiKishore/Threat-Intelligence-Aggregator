from pathlib import Path

import pytest

from deduplication.deduplicator import IOCDeduplicator
from downloader.downloader import Downloader
from normalizer.normalizer import IOCNormalizer
from parsers.parser_manager import ParserManager
from pipeline.processor import PipelineProcessor
from validators.validator import IOCValidator


@pytest.fixture
def pipeline():
    return PipelineProcessor(
        downloader=Downloader(output_dir=Path("feeds/local")),
        parser_manager=ParserManager(),
        validator=IOCValidator(),
        normalizer=IOCNormalizer(),
        deduplicator=IOCDeduplicator(),
    )