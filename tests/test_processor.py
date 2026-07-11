from pathlib import Path

from pipeline.processor import PipelineProcessor
from normalizer.schema import IOC
from normalizer.normalizer import IOCNormalizer
from deduplication.deduplicator import IOCDeduplicator


class MockDownloader:
    """
    Mock downloader for testing.
    """

    def download(
        self,
        url: str,
        filename: str | None = None,
    ) -> Path:

        return Path("test_feed.json")


class MockParserManager:
    """
    Mock parser manager for testing.
    """

    def parse(
        self,
        file_path: Path,
    ) -> list[IOC]:

        return [
            IOC(
                type="IP",
                value="8.8.8.8",
                sources=["feed1.json"],
                confidence=50,
                tags=["google"],
            ),
            IOC(
                type="IP",
                value="8.8.8.8",
                sources=["feed2.json"],
                confidence=80,
                tags=["dns"],
            ),
        ]

class MockValidator:
    """
    Mock validator for testing.
    """

    def validate(
        self,
        ioc: IOC,
    ) -> bool:

        return True


def test_pipeline_process():

    processor = PipelineProcessor(
        downloader=MockDownloader(),
        parser_manager=MockParserManager(),
        validator=MockValidator(),
        normalizer=IOCNormalizer(),
        deduplicator=IOCDeduplicator(),
    )

    result = processor.process(
        "https://example.com/feed.json"
    )

    assert len(result) == 1

    ioc = result[0]

    assert ioc.type == "ip"
    assert ioc.value == "8.8.8.8"

    assert ioc.confidence == 80
    assert sorted(ioc.sources) == [
        "feed1.json",
        "feed2.json",
    ]

    assert sorted(ioc.tags) == [
        "dns",
        "google",
    ]
