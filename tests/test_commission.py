import pandas as pd
from io import BytesIO
from bot.commission import calculate_commissions


def _to_bytes(df: pd.DataFrame) -> bytes:
    buf = BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()


def test_calculate_commissions():
    data = {
        "Date": [
            "2023-01-15",
            "2023-01-20",
            "2023-02-10",
            "2023-02-15",
            "2023-02-16",
            "2023-03-01",
        ],
        "Operation": ["W1", "W2", "W1", "W2", "W1", "W1"],
        "Country": [
            "Brazil",
            "Brazil",
            "Bolivia",
            "Bolivia",
            "Bolivia",
            "Paraguay",
        ],
        "Currency": ["BRL", "BRL", "BOB", "BOB", "BOB", "PYG"],
        "Received": [100, 0, 50, 0, 100, 200],
        "Paid out": [0, 200, 0, 100, 0, 0],
        "Payout Sum": [0, 0, 0, 0, 5, 0],
    }
    df = pd.DataFrame(data)
    result = calculate_commissions(_to_bytes(df))
    expected = "\n".join([
        "2023-01: 9.00",
        "2023-02: 6.00",
        "2023-03: 16.00",
        "Total: 31.00",
    ])
    assert result == expected


def test_missing_columns():
    df = pd.DataFrame({"Date": ["2023-01-01"]})
    try:
        calculate_commissions(_to_bytes(df))
    except ValueError as exc:
        assert "Missing columns" in str(exc)
    else:
        assert False, "ValueError not raised"
