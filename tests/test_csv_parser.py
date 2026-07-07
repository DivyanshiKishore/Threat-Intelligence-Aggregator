from pathlib import Path

from parsers.csv_parser import CSVParser


def test_parse_csv(tmp_path: Path):

    file = tmp_path / "feed.csv"

    file.write_text(
        "type,value\nip,8.8.8.8\n",
        encoding="utf-8"
    )

    parser = CSVParser()

    result = parser.parse(file)

    assert len(result) == 1

    assert result[0].type == "ip"
    assert result[0].value == "8.8.8.8"
    assert result[0].source == "feed.csv"