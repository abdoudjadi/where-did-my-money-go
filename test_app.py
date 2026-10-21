
import pandas as pd

from app import validate_transactions, detect_anomalies


def test_validate_transactions_removes_invalid_rows():
    data = pd.DataFrame({
        "Date": ["2026-10-01", "invalid-date", "2026-10-03"],
        "Category": ["Food", "Food", "Transport"],
        "Description": ["Lunch", "Bad date", "Bus"],
        "Amount": [25.0, 30.0, -5.0],
    })

    cleaned, error = validate_transactions(data)

    assert error is None
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["Amount"] == 25.0


def test_validate_transactions_reports_missing_columns():
    data = pd.DataFrame({
        "Date": ["2026-10-01"],
        "Amount": [25.0],
    })

    cleaned, error = validate_transactions(data)

    assert cleaned is None
    assert "Missing required columns" in error


def test_anomaly_detector_returns_expected_columns():
    data = pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-10-01",
            "2026-10-02",
            "2026-10-03",
            "2026-10-04",
            "2026-10-05",
            "2026-10-06",
        ]),
        "Category": ["Food"] * 6,
        "Description": ["Transaction"] * 6,
        "Amount": [10.0, 12.0, 11.0, 9.0, 13.0, 950.0],
    })

    result = detect_anomalies(data)

    assert "Anomaly" in result.columns
    assert "Anomaly Score" in result.columns
    assert "Reason" in result.columns
    assert len(result) == len(data)


def test_anomaly_detector_handles_small_datasets():
    data = pd.DataFrame({
        "Date": pd.to_datetime(["2026-10-01", "2026-10-02"]),
        "Category": ["Food", "Transport"],
        "Description": ["Lunch", "Bus"],
        "Amount": [10.0, 20.0],
    })

    result = detect_anomalies(data)

    assert (result["Anomaly"] == "Not evaluated").all()
