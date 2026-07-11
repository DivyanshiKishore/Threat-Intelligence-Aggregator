from pathlib import Path
import csv
import json

from exporter.csv_exporter import CSVExporter
from exporter.json_exporter import JSONExporter


def test_pipeline_process_local_txt(pipeline):
    iocs = pipeline.process_file(
        Path("feeds/local/sample.txt")
    )

    assert len(iocs) == 3


def test_pipeline_process_local_csv(pipeline):
    iocs = pipeline.process_file(
        Path("feeds/local/sample.csv")
    )

    assert len(iocs) == 3


def test_pipeline_process_local_json(pipeline):
    iocs = pipeline.process_file(
        Path("feeds/local/sample.json")
    )

    assert len(iocs) == 2


def test_pipeline_filters_invalid_iocs(pipeline):
    iocs = pipeline.process_file(
        Path("feeds/local/sample_invalid.txt")
    )

    assert len(iocs) == 3


def test_pipeline_removes_duplicates(pipeline):
    iocs = pipeline.process_file(
        Path("feeds/local/sample_duplicates.txt")

    )

    assert len(iocs) == 3
    assert all(ioc.value for ioc in iocs)


def test_json_export_integration(pipeline, tmp_path):
    iocs = pipeline.process_file(
        Path("feeds/local/sample.json")

    )

    output_file = tmp_path / "output.json"

    exporter = JSONExporter()
    exporter.export(iocs, output_file)

    assert output_file.exists()

    exported = json.loads(output_file.read_text())

    assert len(exported) == len(iocs)

    for item, ioc in zip(exported, iocs):
        assert item["type"] == ioc.type
        assert item["value"] == ioc.value



def test_csv_export_integration(pipeline, tmp_path):
    iocs = pipeline.process_file(
        Path("feeds/local/sample.json")
    )

    output_file = tmp_path / "output.csv"

    exporter = CSVExporter()
    exporter.export(iocs, output_file)

    assert output_file.exists()

    with output_file.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == len(iocs)

    for row, ioc in zip(rows, iocs):
        assert row["type"] == ioc.type
        assert row["value"] == ioc.value


def test_pipeline_normalizes_iocs(pipeline):
    iocs = pipeline.process_file(
        Path("feeds/local/sample_normalization.json")
    )

    assert len(iocs) == 1
    

    assert iocs[0].type == "url"
    assert iocs[0].value == "https://example.com/Login"