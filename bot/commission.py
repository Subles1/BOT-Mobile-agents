"""Commission report utilities for Telegram bot."""

from __future__ import annotations

from io import BytesIO
from typing import Dict

import pandas as pd

# Country specific commission percentages
COUNTRY_RATES: Dict[str, float] = {
    "Kazakhstan": 0.05,
    "Russia": 0.07,
}
# Default percentage if country is not found in COUNTRY_RATES
DEFAULT_RATE = 0.05

def calculate_commissions(file_bytes: bytes) -> str:
    """Parse XLSX file bytes and return formatted commission report."""
    df = pd.read_excel(BytesIO(file_bytes))

    required = {"Operation", "Country", "Date", "Amount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    df = df[df["Operation"] == "W1=W2"].copy()
    if df.empty:
        return "No operations matching W1=W2"

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    df["Rate"] = df["Country"].map(COUNTRY_RATES).fillna(DEFAULT_RATE)
    df["Commission"] = df["Amount"] * df["Rate"]

    grouped = df.groupby("Month")["Commission"].sum().reset_index()

    lines = []
    total = 0.0
    for _, row in grouped.iterrows():
        month_str = row["Month"].strftime("%Y-%m")
        value = float(row["Commission"])
        total += value
        lines.append(f"{month_str}: {value:.2f}")
    lines.append(f"Total: {total:.2f}")
    return "\n".join(lines)
