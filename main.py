"""Command-line utilities for quick exploration of the project datasets.

This module provides command-line functions for demonstrating the EPA air quality
data analysis capabilities and synthetic sales data generation features of the
GDAPC-Dutta data analysis project.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from AirQuality_Analysis.ada_c2_labs import fetch_epa, sales_data_generator
from utils.logging_utils import get_logger, log_function_call
from utils.validation import validate_positive_int, validate_range

# Initialize logger
logger = get_logger(__name__)


def print_hi(name: str) -> None:
    """Print a friendly greeting to the console.
    
    Args:
        name: Name to greet. Should not be empty.
        
    Raises:
        ValueError: If name is empty or only whitespace.
    """
    log_function_call("print_hi", (name,), {})
    
    if not name or not name.strip():
        raise ValueError("Name cannot be empty or whitespace only")
    
    greeting = f"Hi, {name.strip()}!"
    print(greeting)
    logger.info(f"Displayed greeting: {greeting}")


def preview_air_quality_records(limit: int = 5, csv_path: Optional[Path] = None) -> None:
    """Display a short preview of the EPA air quality dataset.

    Args:
        limit: Number of records to show. Must be between 1 and 100.
        csv_path: Optional path to the EPA CSV file. If None, uses the default.
        
    Raises:
        ValueError: If limit is not in the valid range.
        FileNotFoundError: If the CSV file is not found.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file cannot be parsed.
    """
    log_function_call("preview_air_quality_records", (limit,), {"csv_path": csv_path})
    
    # Validate inputs
    validate_range(limit, "limit", min_val=1, max_val=100)
    
    try:
        logger.info(f"Fetching EPA air quality data preview (limit: {limit})")
        
        states = fetch_epa("state", csv_path) if csv_path else fetch_epa("state")
        counties = fetch_epa("county", csv_path) if csv_path else fetch_epa("county")
        quality = fetch_epa("aqi", csv_path) if csv_path else fetch_epa("aqi")

        print("EPA Air Quality sample:")
        for i, (state, county, aqi) in enumerate(zip(states[:limit], counties[:limit], quality[:limit])):
            print(f"  - {state}, {county}: AQI {aqi}")
            
        logger.info(f"Successfully displayed {min(limit, len(states))} air quality records")
        
    except Exception as e:
        logger.error(f"Error displaying air quality preview: {e}")
        print(f"Error: Unable to display air quality data. {e}")
        raise


def summarize_sales(n_customers: int = 3, seed: int = 42) -> None:
    """Summarise synthetic sales data for a subset of customers.

    Args:
        n_customers: Number of customers to include in the summary.
            Must be between 1 and 1000.
        seed: Seed value used to generate deterministic sample data.
            Must be an integer.
            
    Raises:
        ValueError: If n_customers is not in the valid range.
        TypeError: If seed is not an integer.
        MemoryError: If n_customers is too large for available memory.
    """
    log_function_call("summarize_sales", (n_customers,), {"seed": seed})
    
    # Validate inputs
    validate_range(n_customers, "n_customers", min_val=1, max_val=1000)
    
    try:
        logger.info(f"Generating sales summary for {n_customers} customers (seed: {seed})")
        sales = sales_data_generator(n_customers, seed)

        print("Synthetic sales summary:")
        total_revenue = 0.0
        total_purchases = 0
        
        for index, customer_sales in enumerate(sales, start=1):
            customer_total = sum(customer_sales)
            total_revenue += customer_total
            total_purchases += len(customer_sales)
            
            purchase_summary = ", ".join(f"${amount:.2f}" for amount in customer_sales)
            details = purchase_summary or "no purchases"
            
            print(
                f"  - Customer {index}: {len(customer_sales)} purchases, "
                f"total ${customer_total:.2f} ({details})"
            )
        
        # Display summary statistics
        avg_per_customer = total_revenue / n_customers if n_customers > 0 else 0
        avg_per_purchase = total_revenue / total_purchases if total_purchases > 0 else 0
        
        print(f"\nSummary Statistics:")
        print(f"  - Total customers: {n_customers}")
        print(f"  - Total purchases: {total_purchases}")
        print(f"  - Total revenue: ${total_revenue:.2f}")
        print(f"  - Average per customer: ${avg_per_customer:.2f}")
        print(f"  - Average per purchase: ${avg_per_purchase:.2f}")
        
        logger.info(
            f"Sales summary completed: {total_purchases} purchases, "
            f"${total_revenue:.2f} total revenue"
        )
        
    except Exception as e:
        logger.error(f"Error generating sales summary: {e}")
        print(f"Error: Unable to generate sales summary. {e}")
        raise


if __name__ == "__main__":
    """Main execution block with comprehensive error handling."""
    
    try:
        logger.info("Starting GDAPC-Dutta data analysis demo")
        
        # Display greeting
        print_hi("GDAPC community")
        
        # Display air quality preview
        preview_air_quality_records()
        
        # Display sales summary
        summarize_sales()
        
        logger.info("Demo completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        print("\nDemo interrupted by user.")
        
    except Exception as e:
        logger.critical(f"Demo failed with error: {e}")
        print(f"\nDemo failed: {e}")
        print("Check the logs for more details.")
        
    finally:
        logger.info("Demo execution finished")
