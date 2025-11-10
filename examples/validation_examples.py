#!/usr/bin/env python3
"""Example usage script for data validation utilities.

This script demonstrates how to use the validation utilities for
input validation and error handling in data processing workflows.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logging_utils import setup_logger
from utils.validation import (
    validate_file_path,
    validate_positive_int,
    validate_range,
    validate_literal,
    validate_seed,
    validate_directory_path,
)


def demonstrate_file_validation():
    """Demonstrate file path validation."""
    print("=== File Path Validation Examples ===")
    
    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("test,data\n1,2\n")
        temp_file = Path(f.name)
    
    try:
        # Valid file path
        print("1. Valid file path validation:")
        try:
            validated = validate_file_path(temp_file, must_exist=True, expected_extensions=[".csv"])
            print(f"   ✓ Validated: {validated}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Invalid extension
        print("2. Invalid extension validation:")
        try:
            validate_file_path(temp_file, must_exist=True, expected_extensions=[".txt", ".json"])
        except ValueError as e:
            print(f"   ✓ Caught expected error: {e}")
        
        # Non-existent file
        print("3. Non-existent file validation:")
        try:
            validate_file_path(Path("non_existent.csv"), must_exist=True)
        except FileNotFoundError as e:
            print(f"   ✓ Caught expected error: {e}")
        
        # Allow non-existent file
        print("4. Allow non-existent file:")
        try:
            validated = validate_file_path(Path("future_file.csv"), must_exist=False)
            print(f"   ✓ Validated future path: {validated}")
        except Exception as e:
            print(f"   ✗ Unexpected error: {e}")
            
    finally:
        temp_file.unlink()


def demonstrate_numeric_validation():
    """Demonstrate numeric validation."""
    print("\n=== Numeric Validation Examples ===")
    
    # Positive integer validation
    print("1. Positive integer validation:")
    test_values = [5, 1, 0, -3, 1000000]
    for value in test_values:
        try:
            result = validate_positive_int(value, "test_value")
            print(f"   ✓ {value} -> {result}")
        except ValueError as e:
            print(f"   ✗ {value} -> Error: {e}")
    
    # Range validation
    print("2. Range validation:")
    test_ranges = [
        (5, 1, 10),   # Valid
        (0, 1, 10),   # Below min
        (15, 1, 10),  # Above max
        (5, None, 10), # Only max
        (5, 1, None),  # Only min
    ]
    
    for value, min_val, max_val in test_ranges:
        try:
            result = validate_range(value, "test_value", min_val, max_val)
            print(f"   ✓ {value} (range: {min_val}-{max_val}) -> {result}")
        except ValueError as e:
            print(f"   ✗ {value} (range: {min_val}-{max_val}) -> Error: {e}")


def demonstrate_literal_validation():
    """Demonstrate literal validation."""
    print("\n=== Literal Validation Examples ===")
    
    valid_colors = ["red", "green", "blue"]
    test_values = ["red", "yellow", "GREEN", "", None]
    
    for value in test_values:
        try:
            result = validate_literal(value, valid_colors, "color")
            print(f"   ✓ '{value}' -> {result}")
        except ValueError as e:
            print(f"   ✗ '{value}' -> Error: {e}")


def demonstrate_seed_validation():
    """Demonstrate seed validation."""
    print("\n=== Seed Validation Examples ===")
    
    test_seeds = [42, 0, -5, None, "42", 3.14]
    
    for seed in test_seeds:
        try:
            result = validate_seed(seed)
            print(f"   ✓ {seed} -> {result}")
        except (TypeError, ValueError) as e:
            print(f"   ✗ {seed} -> Error: {e}")


def demonstrate_directory_validation():
    """Demonstrate directory validation."""
    print("\n=== Directory Validation Examples ===")
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Valid existing directory
        print("1. Valid existing directory:")
        try:
            validated = validate_directory_path(temp_path, must_exist=True)
            print(f"   ✓ Validated: {validated}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Create new directory
        print("2. Create new directory:")
        new_dir = temp_path / "new_subdir"
        try:
            validated = validate_directory_path(new_dir, must_exist=False, create_if_missing=True)
            print(f"   ✓ Created and validated: {validated}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Non-existent directory (no creation)
        print("3. Non-existent directory (no creation):")
        missing_dir = temp_path / "missing"
        try:
            validate_directory_path(missing_dir, must_exist=True)
        except FileNotFoundError as e:
            print(f"   ✓ Caught expected error: {e}")


def demonstrate_comprehensive_validation():
    """Demonstrate comprehensive validation in a workflow."""
    print("\n=== Comprehensive Validation Workflow ===")
    
    def process_data_file(file_path, limit, quality_threshold, seed):
        """Example function with comprehensive validation."""
        print(f"\nProcessing data file: {file_path}")
        
        # Validate all inputs
        validated_path = validate_file_path(
            file_path, 
            must_exist=True, 
            expected_extensions=[".csv", ".json"]
        )
        
        validated_limit = validate_range(limit, "limit", min_val=1, max_val=1000)
        
        validated_quality = validate_range(
            quality_threshold, 
            "quality_threshold", 
            min_val=0.0, 
            max_val=1.0
        )
        
        validated_seed = validate_seed(seed)
        
        print(f"   ✓ File path validated: {validated_path}")
        print(f"   ✓ Limit validated: {validated_limit}")
        print(f"   ✓ Quality threshold validated: {validated_quality}")
        print(f"   ✓ Seed validated: {validated_seed}")
        
        # Simulate processing
        print(f"   Processing {validated_limit} records with quality >= {validated_quality}")
        return f"Processed {validated_limit} records successfully"
    
    # Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,value,quality\n1,100,0.95\n2,85,0.87\n")
        test_file = Path(f.name)
    
    try:
        # Valid processing
        print("1. Valid processing parameters:")
        result = process_data_file(test_file, 100, 0.8, 42)
        print(f"   Result: {result}")
        
        # Invalid parameters
        print("\n2. Invalid file extension:")
        try:
            process_data_file(test_file.with_suffix('.txt'), 100, 0.8, 42)
        except (ValueError, FileNotFoundError) as e:
            print(f"   ✓ Caught expected error: {e}")
        
        print("\n3. Invalid limit:")
        try:
            process_data_file(test_file, 0, 0.8, 42)
        except ValueError as e:
            print(f"   ✓ Caught expected error: {e}")
        
        print("\n4. Invalid quality threshold:")
        try:
            process_data_file(test_file, 100, 1.5, 42)
        except ValueError as e:
            print(f"   ✓ Caught expected error: {e}")
            
    finally:
        test_file.unlink()


def main():
    """Run all validation demonstrations."""
    
    # Set up logging
    logger = setup_logger(
        "validation_example",
        level="INFO",
        log_file="validation_examples.log"
    )
    
    logger.info("Starting validation examples demonstration")
    
    try:
        demonstrate_file_validation()
        demonstrate_numeric_validation()
        demonstrate_literal_validation()
        demonstrate_seed_validation()
        demonstrate_directory_validation()
        demonstrate_comprehensive_validation()
        
        logger.info("Validation examples completed successfully")
        print("\n" + "="*50)
        print("All validation examples completed successfully!")
        print("Detailed logs saved to: validation_examples.log")
        
    except Exception as e:
        logger.error(f"Error in validation examples: {e}")
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()