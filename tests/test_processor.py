from pathlib import Path

from pipeline.processor import PipelineProcessor
from normalizer.schema import IOC
from normalizer.normalizer import IOCNormalizer


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
                source="test_feed.json",
            ),
            IOC(
                type="DOMAIN",
                value="Example.COM  ",
                source="test_feed.json",
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
    )

    result = processor.process(
        "https://example.com/feed.json"
    )

    assert len(result) == 2

    assert result[0].type == "ip"
    assert result[0].value == "8.8.8.8"

    assert result[1].type == "domain"
    assert result[1].value == "example.com"