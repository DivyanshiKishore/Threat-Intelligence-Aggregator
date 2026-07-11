from pathlib import Path

from exporter.csv_exporter import CSVExporter
from exporter.json_exporter import JSONExporter
from normalizer.schema import IOC


def sample_iocs():
    return [
        IOC(
            type="ip",
            value="8.8.8.8",
            sources=["test_feed"],
            confidence=90,
            tags=["dns", "google"],
            first_seen=None,
            last_seen=None,
        )
    ]


def test_csv_exporter(tmp_path: Path):
    output = tmp_path / "iocs.csv"

    CSVExporter().export(sample_iocs(), output)

    assert output.exists()

    content = output.read_text(encoding="utf-8")
    assert "8.8.8.8" in content
    assert "google" in content


def test_json_exporter(tmp_path: Path):
    output = tmp_path / "iocs.json"

    JSONExporter().export(sample_iocs(), output)

    assert output.exists()

    content = output.read_text(encoding="utf-8")
    assert '"value": "8.8.8.8"' in content
    assert '"type": "ip"' in content