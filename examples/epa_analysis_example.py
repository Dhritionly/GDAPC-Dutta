#!/usr/bin/env python3
"""Example usage script for EPA air quality data analysis.

This script demonstrates various ways to use the EPA data analysis functions
with different parameters and error handling scenarios.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import tempfile

from AirQuality_Analysis.ada_c2_labs import fetch_epa, lists_gen
from utils.logging_utils import setup_logger
from utils.validation import validate_file_path


def main():
    """Demonstrate EPA data analysis capabilities."""
    
    # Set up detailed logging
    logger = setup_logger(
        "epa_example",
        level="DEBUG",
        log_file="epa_analysis.log"
    )
    
    logger.info("Starting EPA air quality data analysis example")
    
    try:
        # Example 1: Basic data fetching
        print("=== Example 1: Basic EPA Data Fetching ===")
        
        states = fetch_epa("state")
        counties = fetch_epa("county")
        aqi_values = fetch_epa("aqi")
        
        print(f"Loaded {len(states)} records")
        print(f"Sample states: {states[:5]}")
        print(f"Sample counties: {counties[:5]}")
        print(f"Sample AQI values: {aqi_values[:5]}")
        
        # Example 2: Data analysis
        print("\n=== Example 2: Air Quality Analysis ===")
        
        # Calculate statistics
        aqi_stats = {
            "min": min(aqi_values),
            "max": max(aqi_values),
            "average": sum(aqi_values) / len(aqi_values),
            "count": len(aqi_values)
        }
        
        print(f"AQI Statistics:")
        for key, value in aqi_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")
        
        # Categorize air quality
        good_days = sum(1 for aqi in aqi_values if aqi <= 50)
        moderate_days = sum(1 for aqi in aqi_values if 51 <= aqi <= 100)
        unhealthy_days = sum(1 for aqi in aqi_values if aqi > 100)
        
        print(f"\nAir Quality Categories:")
        print(f"  Good (0-50): {good_days} days ({good_days/len(aqi_values)*100:.1f}%)")
        print(f"  Moderate (51-100): {moderate_days} days ({moderate_days/len(aqi_values)*100:.1f}%)")
        print(f"  Unhealthy (>100): {unhealthy_days} days ({unhealthy_days/len(aqi_values)*100:.1f}%)")
        
        # Example 3: Generate sample IDs for data tracking
        print("\n=== Example 3: Generate Sample Tracking IDs ===")
        
        verified_ids, feedback_ids = lists_gen(
            n_chars_id=8,
            n_pool=1000,
            n_feedback_ids=50,
            n_verified_ids=75,
            seed=42
        )
        
        print(f"Generated {len(verified_ids)} verified IDs")
        print(f"Generated {len(feedback_ids)} feedback IDs")
        print(f"Sample verified IDs: {verified_ids[:5]}")
        print(f"Sample feedback IDs: {feedback_ids[:5]}")
        
        # Example 4: Working with custom data files
        print("\n=== Example 4: Custom Data File Processing ===")
        
        # Create a sample CSV file
        sample_data = """state_name,county_name,aqi
California,San Diego,35
Texas,Dallas,65
New York,Albany,28
Florida,Miami,85
Illinois,Chicago,72"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(sample_data)
            sample_file = Path(f.name)
        
        try:
            # Load data from custom file
            custom_states = fetch_epa("state", sample_file)
            custom_counties = fetch_epa("county", sample_file)
            custom_aqi = fetch_epa("aqi", sample_file)
            
            print(f"Loaded {len(custom_states)} records from custom file")
            for state, county, aqi in zip(custom_states, custom_counties, custom_aqi):
                print(f"  {state}, {county}: AQI {aqi}")
                
        finally:
            sample_file.unlink()
        
        logger.info("EPA air quality data analysis example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in EPA analysis example: {e}")
        print(f"Error: {e}")
        raise
    
    finally:
        print(f"\nDetailed logs saved to: epa_analysis.log")


if __name__ == "__main__":
    main()