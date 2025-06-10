"""Commission report utilities for Telegram bot."""

from __future__ import annotations

from io import BytesIO
from typing import Dict

import pandas as pd

# Country specific commission percentages
# Values represent the commission taken from deposits for each country.
COUNTRY_RATES: Dict[str, float] = {
    "Algeria": 0.05,
    "Argentina": 0.05,
    "Azerbaijan": 0.06,
    "Bangladesh": 0.05,
    "Benin": 0.05,
    "Bolivia": 0.08,
    "Brazil": 0.05,
    "Burkina Faso": 0.05,
    "Cameroon": 0.05,
    "Colombia": 0.05,
    "Congo (Kinshasa)": 0.05,
    "Cote D'Ivoire": 0.05,
    "Djibouti": 0.05,
    "Ecuador": 0.05,
    "Egypt": 0.05,
    "Gabon": 0.05,
    "Guinea": 0.05,
    "Haiti": 0.05,
    "India": 0.05,
    "Iran": 0.05,
    "Kyrgyzstan": 0.08,
    "Madagascar": 0.05,
    "Morocco": 0.05,
    "Nepal": 0.05,
    "Niger": 0.05,
    "Pakistan": 0.05,
    "Somalia": 0.05,
    "Sri Lanka": 0.05,
    "Togo": 0.05,
    "Tunisia": 0.05,
    "Turkey": 0.08,
    "Turkmenistan": 0.08,
    "Uzbekistan": 0.08,
    "Venezuela": 0.05,
    "Zambia": 0.05,
    "Paraguay": 0.08,
}
# Default percentage if country is not found in COUNTRY_RATES
DEFAULT_RATE = 0.05

def calculate_commissions(file_bytes: bytes) -> str:
    """Parse XLSX file bytes and return formatted commission report."""
    df = pd.read_excel(BytesIO(file_bytes))

    required = {
        "Date",
        "Operation",
        "Country",
        "Currency",
        "Received",
        "Paid out",
        "Payout Sum",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

    # Ignore rows with non-zero cancellation amounts
    df = df[df["Payout Sum"] == 0].copy()
    if df.empty:
        return "No valid operations found"

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    deposits = df[df["Operation"] == "W1"].copy()
    deposits["Rate"] = deposits["Country"].map(COUNTRY_RATES).fillna(DEFAULT_RATE)
    deposits["Commission"] = deposits["Received"] * deposits["Rate"]

    withdrawals = df[df["Operation"] == "W2"].copy()
    withdrawals["Commission"] = withdrawals["Paid out"] * 0.02

    grouped = (
        pd.concat(
            [deposits[["Month", "Commission"]], withdrawals[["Month", "Commission"]]],
            ignore_index=True,
        )
        .groupby("Month")["Commission"]
        .sum()
        .sort_index()
    )

    lines = []
    total = 0.0
    for month, value in grouped.items():
        month_str = month.strftime("%Y-%m")
        value = float(value)
        total += value
        lines.append(f"{month_str}: {value:.2f}")
    lines.append(f"Total: {total:.2f}")
    return "\n".join(lines)
