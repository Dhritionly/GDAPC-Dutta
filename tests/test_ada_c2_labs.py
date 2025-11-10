"""Test suite for the ada_c2_labs module."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from AirQuality_Analysis.ada_c2_labs import (
    fetch_epa,
    id_gen,
    lists_gen,
    sales_data_generator,
)


class TestFetchEPA(unittest.TestCase):
    """Test cases for the fetch_epa function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            "state_name": ["California", "Texas", "New York"],
            "county_name": ["Los Angeles", "Harris", "New York"],
            "aqi": [45, 67, 32]
        }
        self.test_df = pd.DataFrame(self.test_data)
        
    def test_fetch_epa_state(self):
        """Test fetching state data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_df.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            result = fetch_epa("state", temp_path)
            self.assertEqual(result, self.test_data["state_name"])
        finally:
            temp_path.unlink()
    
    def test_fetch_epa_county(self):
        """Test fetching county data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_df.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            result = fetch_epa("county", temp_path)
            self.assertEqual(result, self.test_data["county_name"])
        finally:
            temp_path.unlink()
    
    def test_fetch_epa_aqi(self):
        """Test fetching AQI data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_df.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            result = fetch_epa("aqi", temp_path)
            self.assertEqual(result, self.test_data["aqi"])
        finally:
            temp_path.unlink()
    
    def test_fetch_epa_invalid_key(self):
        """Test fetch_epa with invalid key."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_df.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            with self.assertRaises(ValueError):
                fetch_epa("invalid", temp_path)
        finally:
            temp_path.unlink()
    
    def test_fetch_epa_file_not_found(self):
        """Test fetch_epa with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            fetch_epa("state", "non_existent.csv")
    
    def test_fetch_epa_missing_column(self):
        """Test fetch_epa with missing required column."""
        incomplete_data = {"other_column": [1, 2, 3]}
        incomplete_df = pd.DataFrame(incomplete_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            incomplete_df.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            with self.assertRaises(ValueError):
                fetch_epa("state", temp_path)
        finally:
            temp_path.unlink()


class TestIdGen(unittest.TestCase):
    """Test cases for the id_gen function."""
    
    def test_id_gen_basic(self):
        """Test basic ID generation."""
        result = id_gen(6, 10)
        self.assertEqual(len(result), 10)
        self.assertTrue(all(len(id_str) == 6 for id_str in result))
        self.assertTrue(all(c.isalnum() for id_str in result for c in id_str))
    
    def test_id_gen_deterministic(self):
        """Test that ID generation is deterministic."""
        result1 = id_gen(8, 5)
        result2 = id_gen(8, 5)
        self.assertEqual(result1, result2)
    
    def test_id_gen_different_lengths(self):
        """Test ID generation with different lengths."""
        for length in [1, 5, 10, 20]:
            result = id_gen(length, 3)
            self.assertTrue(all(len(id_str) == length for id_str in result))
    
    def test_id_gen_invalid_inputs(self):
        """Test id_gen with invalid inputs."""
        with self.assertRaises(ValueError):
            id_gen(0, 10)
        
        with self.assertRaises(ValueError):
            id_gen(5, 0)
        
        with self.assertRaises(ValueError):
            id_gen(101, 10)  # Too long
        
        with self.assertRaises(MemoryError):
            id_gen(5, 1000001)  # Too many samples


class TestListsGen(unittest.TestCase):
    """Test cases for the lists_gen function."""
    
    def test_lists_gen_basic(self):
        """Test basic list generation."""
        verified, feedback = lists_gen(6, 100, 10, 15, seed=42)
        
        self.assertEqual(len(verified), 15)
        self.assertEqual(len(feedback), 10)
        self.assertTrue(all(len(id_str) == 6 for id_str in verified + feedback))
        self.assertTrue(all(c.isalnum() for id_str in verified + feedback for c in id_str))
    
    def test_lists_gen_deterministic(self):
        """Test that list generation is deterministic."""
        verified1, feedback1 = lists_gen(6, 50, 5, 8, seed=123)
        verified2, feedback2 = lists_gen(6, 50, 5, 8, seed=123)
        
        self.assertEqual(verified1, verified2)
        self.assertEqual(feedback1, feedback2)
    
    def test_lists_gen_pool_too_small(self):
        """Test lists_gen with pool too small."""
        with self.assertRaises(ValueError):
            lists_gen(6, 10, 15, 5)  # Pool smaller than feedback
        
        with self.assertRaises(ValueError):
            lists_gen(6, 10, 5, 15)  # Pool smaller than verified
        
        with self.assertRaises(ValueError):
            lists_gen(6, 10, 8, 8)  # Pool smaller than combined
    
    def test_lists_gen_zero_samples(self):
        """Test lists_gen with zero samples."""
        verified, feedback = lists_gen(6, 10, 0, 0)
        self.assertEqual(len(verified), 0)
        self.assertEqual(len(feedback), 0)


class TestSalesDataGenerator(unittest.TestCase):
    """Test cases for the sales_data_generator function."""
    
    def test_sales_data_generator_basic(self):
        """Test basic sales data generation."""
        result = sales_data_generator(5, seed=42)
        
        self.assertEqual(len(result), 5)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(all(isinstance(customer_sales, list) for customer_sales in result))
        self.assertTrue(all(isinstance(amount, (int, float)) for customer_sales in result for amount in customer_sales))
    
    def test_sales_data_generator_deterministic(self):
        """Test that sales data generation is deterministic."""
        result1 = sales_data_generator(3, seed=123)
        result2 = sales_data_generator(3, seed=123)
        
        self.assertEqual(result1, result2)
    
    def test_sales_data_generator_range(self):
        """Test sales data generation with different customer counts."""
        for n_customers in [1, 5, 10, 50]:
            result = sales_data_generator(n_customers, seed=42)
            self.assertEqual(len(result), n_customers)
    
    def test_sales_data_generator_purchases_per_customer(self):
        """Test that each customer has 0-6 purchases."""
        result = sales_data_generator(100, seed=42)
        
        for customer_sales in result:
            self.assertGreaterEqual(len(customer_sales), 0)
            self.assertLessEqual(len(customer_sales), 6)
    
    def test_sales_data_generator_invalid_inputs(self):
        """Test sales_data_generator with invalid inputs."""
        with self.assertRaises(ValueError):
            sales_data_generator(0, 42)
        
        with self.assertRaises(ValueError):
            sales_data_generator(-5, 42)
        
        with self.assertRaises(TypeError):
            sales_data_generator(5, "not_an_int")
        
        with self.assertRaises(MemoryError):
            sales_data_generator(1000001, 42)


if __name__ == "__main__":
    unittest.main()