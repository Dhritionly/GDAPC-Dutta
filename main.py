"""Command-line utilities for quick exploration of the project datasets."""

from __future__ import annotations

from AirQuality_Analysis.ada_c2_labs import fetch_epa, sales_data_generator


def print_hi(name: str) -> None:
    """Print a friendly greeting to the console."""
    print(f"Hi, {name}!")


def preview_air_quality_records(limit: int = 5) -> None:
    """Display a short preview of the EPA air quality dataset.

    Args:
        limit: Number of records to show.
    """
    states = fetch_epa("state")
    counties = fetch_epa("county")
    quality = fetch_epa("aqi")

    print("EPA Air Quality sample:")
    for state, county, aqi in zip(states[:limit], counties[:limit], quality[:limit]):
        print(f"  - {state}, {county}: AQI {aqi}")


def summarize_sales(n_customers: int = 3, seed: int = 42) -> None:
    """Summarise synthetic sales data for a subset of customers.

    Args:
        n_customers: Number of customers to include in the summary.
        seed: Seed value used to generate deterministic sample data.
    """
    sales = sales_data_generator(n_customers, seed)

    print("Synthetic sales summary:")
    for index, customer_sales in enumerate(sales, start=1):
        total = sum(customer_sales)
        purchase_summary = ", ".join(f"${amount:.2f}" for amount in customer_sales)
        details = purchase_summary or "no purchases"
        print(
            f"  - Customer {index}: {len(customer_sales)} purchases, "
            f"total ${total:.2f} ({details})"
        )


if __name__ == "__main__":
    print_hi("GDAPC community")
    preview_air_quality_records()
    summarize_sales()
