from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from downloader.downloader import Downloader
from downloader.exceptions import DownloaderError


def test_successful_download(tmp_path: Path):
    """
    Test successful feed download.
    """

    downloader = Downloader(
        output_dir=tmp_path
    )

    mock_response = Mock()
    mock_response.text = "8.8.8.8"
    mock_response.raise_for_status = Mock()

    with patch(
        "downloader.downloader.requests.get",
        return_value=mock_response,
    ):

        result = downloader.download(
            "https://example.com/feed.txt"
        )

    assert result.exists()
    assert result.read_text() == "8.8.8.8"


def test_download_with_custom_filename(tmp_path: Path):
    """
    Test custom output filename.
    """

    downloader = Downloader(
        output_dir=tmp_path
    )

    mock_response = Mock()
    mock_response.text = "example.com"
    mock_response.raise_for_status = Mock()

    with patch(
        "downloader.downloader.requests.get",
        return_value=mock_response,
    ):

        result = downloader.download(
            "https://example.com/feed",
            filename="custom.txt",
        )

    assert result.name == "custom.txt"


def test_download_failure(tmp_path: Path):
    """
    Test failed download after retries.
    """

    downloader = Downloader(
        output_dir=tmp_path,
        retries=2,
    )

    with patch(
        "downloader.downloader.requests.get",
        side_effect=requests.RequestException,
    ):

        with pytest.raises(DownloaderError):
            downloader.download(
                "https://example.com/feed.txt"
            )