from reports.summary import Summary


def test_generate_summary():
    statistics = {
        "total": 3,
        "types": {
            "ipv4": 2,
            "domain": 1,
        },
        "sources": {
            "AlienVault": 2,
            "Abuse.ch": 1,
        },
        "confidence": {
            "0-25": 0,
            "26-50": 1,
            "51-75": 1,
            "76-100": 1,
        },
        "tags": {
            "malware": 2,
            "phishing": 1,
        },
    }

    report = Summary.generate(statistics)

    assert "Threat Intelligence Summary" in report
    assert "Total IOCs: 3" in report
    assert "IOC Types" in report
    assert "Sources" in report
    assert "Confidence Distribution" in report
    assert "Tags" in report