#!/usr/bin/env python3
"""Example usage script for sales data generation and analysis.

This script demonstrates various ways to use the sales data generation
functions with different parameters and analysis scenarios.
"""

from __future__ import annotations

import statistics
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from AirQuality_Analysis.ada_c2_labs import sales_data_generator
from utils.logging_utils import setup_logger


def analyze_sales_data(sales_data):
    """Analyze sales data and return statistics.
    
    Args:
        sales_data: List of customer sales data.
        
    Returns:
        Dictionary containing analysis results.
    """
    # Flatten all purchases
    all_purchases = [purchase for customer in sales_data for purchase in customer]
    
    if not all_purchases:
        return {
            "total_customers": len(sales_data),
            "total_purchases": 0,
            "total_revenue": 0.0,
            "avg_purchase": 0.0,
            "median_purchase": 0.0,
            "max_purchase": 0.0,
            "min_purchase": 0.0,
            "customers_with_purchases": 0
        }
    
    return {
        "total_customers": len(sales_data),
        "total_purchases": len(all_purchases),
        "total_revenue": sum(all_purchases),
        "avg_purchase": statistics.mean(all_purchases),
        "median_purchase": statistics.median(all_purchases),
        "max_purchase": max(all_purchases),
        "min_purchase": min(all_purchases),
        "customers_with_purchases": sum(1 for customer in sales_data if customer)
    }


def main():
    """Demonstrate sales data generation and analysis."""
    
    # Set up detailed logging
    logger = setup_logger(
        "sales_example",
        level="DEBUG",
        log_file="sales_analysis.log"
    )
    
    logger.info("Starting sales data generation and analysis example")
    
    try:
        # Example 1: Basic sales data generation
        print("=== Example 1: Basic Sales Data Generation ===")
        
        basic_sales = sales_data_generator(10, seed=42)
        
        print("Generated sales data for 10 customers:")
        for i, customer_sales in enumerate(basic_sales, 1):
            total = sum(customer_sales)
            print(f"  Customer {i}: {len(customer_sales)} purchases, ${total:.2f}")
        
        # Example 2: Comprehensive analysis
        print("\n=== Example 2: Sales Data Analysis ===")
        
        analysis = analyze_sales_data(basic_sales)
        
        print("Sales Analysis Results:")
        for key, value in analysis.items():
            if isinstance(value, float):
                print(f"  {key}: ${value:.2f}")
            else:
                print(f"  {key}: {value}")
        
        # Example 3: Different customer segments
        print("\n=== Example 3: Customer Segment Analysis ===")
        
        # Generate data for different business scenarios
        scenarios = [
            ("Small Business", 50, 123),
            ("Medium Business", 200, 456),
            ("Large Business", 1000, 789),
        ]
        
        for name, customers, seed in scenarios:
            print(f"\n{name} Scenario ({customers} customers):")
            sales = sales_data_generator(customers, seed)
            analysis = analyze_sales_data(sales)
            
            conversion_rate = (analysis["customers_with_purchases"] / analysis["total_customers"]) * 100
            
            print(f"  Total Revenue: ${analysis['total_revenue']:,.2f}")
            print(f"  Average Purchase: ${analysis['avg_purchase']:.2f}")
            print(f"  Conversion Rate: {conversion_rate:.1f}%")
        
        # Example 4: Performance comparison
        print("\n=== Example 4: Performance Comparison ===")
        
        import time
        
        test_sizes = [100, 1000, 5000]
        
        for size in test_sizes:
            start_time = time.time()
            test_sales = sales_data_generator(size, seed=999)
            end_time = time.time()
            
            analysis = analyze_sales_data(test_sales)
            
            print(f"\nSize: {size:,} customers")
            print(f"  Generation time: {(end_time - start_time)*1000:.1f}ms")
            print(f"  Total purchases: {analysis['total_purchases']:,}")
            print(f"  Total revenue: ${analysis['total_revenue']:,.2f}")
        
        # Example 5: Customer behavior patterns
        print("\n=== Example 5: Customer Behavior Patterns ===")
        
        # Generate a larger dataset for pattern analysis
        behavior_sales = sales_data_generator(1000, seed=555)
        
        # Analyze purchase frequency
        purchase_counts = [len(customer) for customer in behavior_sales]
        
        frequency_distribution = {}
        for count in purchase_counts:
            frequency_distribution[count] = frequency_distribution.get(count, 0) + 1
        
        print("Purchase Frequency Distribution:")
        for purchases, customers in sorted(frequency_distribution.items()):
            percentage = (customers / len(behavior_sales)) * 100
            print(f"  {purchases} purchases: {customers} customers ({percentage:.1f}%)")
        
        # Calculate customer value segments
        customer_values = [sum(customer) for customer in behavior_sales]
        customer_values.sort(reverse=True)
        
        # Top 10% customers
        top_10_percent_count = max(1, len(customer_values) // 10)
        top_10_percent_revenue = sum(customer_values[:top_10_percent_count])
        total_revenue = sum(customer_values)
        
        print(f"\nCustomer Value Analysis:")
        print(f"  Top 10% customers: {top_10_percent_count} customers")
        print(f"  Top 10% revenue: ${top_10_percent_revenue:,.2f}")
        print(f"  Top 10% revenue share: {(top_10_percent_revenue/total_revenue)*100:.1f}%")
        
        logger.info("Sales data generation and analysis example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in sales analysis example: {e}")
        print(f"Error: {e}")
        raise
    
    finally:
        print(f"\nDetailed logs saved to: sales_analysis.log")


if __name__ == "__main__":
    main()