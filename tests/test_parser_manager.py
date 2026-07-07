import json
from pathlib import Path

import pytest

from parsers.parser_manager import ParserManager


def test_parse_txt(tmp_path: Path):
    """Test parsing a TXT feed."""

    file = tmp_path / "feed.txt"
    file.write_text("8.8.8.8\n", encoding="utf-8")

    manager = ParserManager()
    result = manager.parse(file)

    assert len(result) == 1
    assert result[0].value == "8.8.8.8"


def test_parse_csv(tmp_path: Path):
    """Test parsing a CSV feed."""

    file = tmp_path / "feed.csv"

    file.write_text(
        "type,value\nip,8.8.8.8\n",
        encoding="utf-8"
    )

    manager = ParserManager()
    result = manager.parse(file)

    assert len(result) == 1
    assert result[0].type == "ip"
    assert result[0].value == "8.8.8.8"


def test_parse_json(tmp_path: Path):
    """Test parsing a JSON feed."""

    file = tmp_path / "feed.json"

    data = [
        {
            "type": "ip",
            "value": "1.1.1.1"
        }
    ]

    file.write_text(
        json.dumps(data),
        encoding="utf-8"
    )

    manager = ParserManager()
    result = manager.parse(file)

    assert len(result) == 1
    assert result[0].type == "ip"
    assert result[0].value == "1.1.1.1"


def test_unsupported_file(tmp_path: Path):
    """Unsupported extensions should raise ValueError."""

    file = tmp_path / "feed.xml"
    file.write_text("<xml></xml>", encoding="utf-8")

    manager = ParserManager()

    with pytest.raises(ValueError):
        manager.parse(file)