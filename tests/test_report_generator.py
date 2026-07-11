from normalizer.schema import IOC
from reports.report_generator import ReportGenerator


def test_generate_report():
    iocs = [
        IOC(
            type="ipv4",
            value="1.1.1.1",
            sources=["AlienVault"],
            confidence=90,
            tags=["malware"],
        ),
        IOC(
            type="domain",
            value="example.com",
            sources=["Abuse.ch"],
            confidence=60,
            tags=["phishing"],
        ),
    ]

    report = ReportGenerator.generate(iocs)

    assert "Threat Intelligence Summary" in report
    assert "Total IOCs: 2" in report
    assert "ipv4" in report
    assert "domain" in report


def test_save_report(tmp_path):
    report = "Example Report"

    output_file = tmp_path / "report.txt"

    ReportGenerator.save(report, str(output_file))

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == report