from pathlib import Path

from parsers.txt_parser import TXTParser


def test_parse_txt(tmp_path: Path):

    file = tmp_path / "feed.txt"

    file.write_text(
        "8.8.8.8\nexample.com\n",
        encoding="utf-8"
    )

    parser = TXTParser()

    result = parser.parse(file)

    assert len(result) == 2

    assert result[0].value == "8.8.8.8"
    assert result[1].value == "example.com"
    assert result[0].sources == ["feed.txt"]