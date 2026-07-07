import json
from pathlib import Path

from parsers.json_parser import JSONParser


def test_parse_json_list(tmp_path: Path):
    file = tmp_path / "feed.json"

    data = [
        {"type": "ip", "value": "8.8.8.8"},
        {"type": "domain", "value": "example.com"},
    ]

    file.write_text(json.dumps(data), encoding="utf-8")

    parser = JSONParser()
    result = parser.parse(file)

    assert len(result) == 2
    assert result[0].type == "ip"
    assert result[1].value == "example.com"


def test_parse_json_iocs_key(tmp_path: Path):
    file = tmp_path / "feed.json"

    data = {
        "iocs": [
            {"type": "hash", "value": "abc123"}
        ]
    }

    file.write_text(json.dumps(data), encoding="utf-8")

    parser = JSONParser()
    result = parser.parse(file)

    assert len(result) == 1
    assert result[0].type == "hash"


def test_parse_single_ioc(tmp_path: Path):
    file = tmp_path / "feed.json"

    data = {
        "type": "ip",
        "value": "1.1.1.1",
    }

    file.write_text(json.dumps(data), encoding="utf-8")

    parser = JSONParser()
    result = parser.parse(file)

    assert len(result) == 1
    assert result[0].value == "1.1.1.1"


def test_invalid_json(tmp_path: Path):
    file = tmp_path / "feed.json"

    file.write_text("{invalid", encoding="utf-8")

    parser = JSONParser()

    result = parser.parse(file)

    assert result == []


def test_unknown_structure(tmp_path: Path):
    file = tmp_path / "feed.json"

    data = {"hello": "world"}

    file.write_text(json.dumps(data), encoding="utf-8")

    parser = JSONParser()

    result = parser.parse(file)

    assert result == []