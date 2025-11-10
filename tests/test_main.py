"""Test suite for the main module."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from main import print_hi, preview_air_quality_records, summarize_sales


class TestPrintHi(unittest.TestCase):
    """Test cases for the print_hi function."""
    
    @patch('builtins.print')
    def test_print_hi_normal(self, mock_print):
        """Test print_hi with normal input."""
        print_hi("World")
        mock_print.assert_called_once_with("Hi, World!")
    
    @patch('builtins.print')
    def test_print_hi_with_whitespace(self, mock_print):
        """Test print_hi with whitespace."""
        print_hi("  Test  ")
        mock_print.assert_called_once_with("Hi, Test!")
    
    @patch('builtins.print')
    def test_print_hi_empty(self, mock_print):
        """Test print_hi with empty string."""
        with self.assertRaises(ValueError):
            print_hi("")
    
    @patch('builtins.print')
    def test_print_hi_whitespace_only(self, mock_print):
        """Test print_hi with whitespace only."""
        with self.assertRaises(ValueError):
            print_hi("   ")


class TestPreviewAirQualityRecords(unittest.TestCase):
    """Test cases for the preview_air_quality_records function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            "state_name": ["California", "Texas", "New York", "Florida", "Ohio"],
            "county_name": ["Los Angeles", "Harris", "New York", "Miami-Dade", "Cuyahoga"],
            "aqi": [45, 67, 32, 78, 23]
        }
        self.test_df = pd.DataFrame(self.test_data)
    
    @patch('builtins.print')
    @patch('main.fetch_epa')
    def test_preview_air_quality_basic(self, mock_fetch, mock_print):
        """Test basic air quality preview."""
        mock_fetch.side_effect = [
            self.test_data["state_name"],
            self.test_data["county_name"],
            self.test_data["aqi"]
        ]
        
        preview_air_quality_records(3)
        
        mock_fetch.assert_any_call("state")
        mock_fetch.assert_any_call("county")
        mock_fetch.assert_any_call("aqi")
        
        # Check that print was called with expected output
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("EPA Air Quality sample:" in call for call in calls))
    
    @patch('builtins.print')
    @patch('main.fetch_epa')
    def test_preview_air_quality_custom_limit(self, mock_fetch, mock_print):
        """Test air quality preview with custom limit."""
        mock_fetch.side_effect = [
            self.test_data["state_name"],
            self.test_data["county_name"],
            self.test_data["aqi"]
        ]
        
        preview_air_quality_records(2)
        
        # Should only call fetch_epa 3 times (state, county, aqi)
        self.assertEqual(mock_fetch.call_count, 3)
    
    def test_preview_air_quality_invalid_limit(self):
        """Test preview_air_quality with invalid limits."""
        with self.assertRaises(ValueError):
            preview_air_quality_records(0)
        
        with self.assertRaises(ValueError):
            preview_air_quality_records(-1)
        
        with self.assertRaises(ValueError):
            preview_air_quality_records(101)
    
    @patch('builtins.print')
    @patch('main.fetch_epa')
    def test_preview_air_quality_with_csv_path(self, mock_fetch, mock_print):
        """Test air quality preview with custom CSV path."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_df.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            mock_fetch.side_effect = [
                self.test_data["state_name"],
                self.test_data["county_name"],
                self.test_data["aqi"]
            ]
            
            preview_air_quality_records(3, csv_path=temp_path)
            
            # Check that fetch_epa was called with the path
            mock_fetch.assert_any_call("state", temp_path)
            mock_fetch.assert_any_call("county", temp_path)
            mock_fetch.assert_any_call("aqi", temp_path)
        finally:
            temp_path.unlink()


class TestSummarizeSales(unittest.TestCase):
    """Test cases for the summarize_sales function."""
    
    @patch('builtins.print')
    @patch('main.sales_data_generator')
    def test_summarize_sales_basic(self, mock_generator, mock_print):
        """Test basic sales summary."""
        mock_generator.return_value = [
            [10.50, 25.75],  # Customer 1
            [5.25],          # Customer 2
            []               # Customer 3 (no purchases)
        ]
        
        summarize_sales(3, seed=42)
        
        mock_generator.assert_called_once_with(3, 42)
        
        # Check that print was called with expected output
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("Synthetic sales summary:" in call for call in calls))
        self.assertTrue(any("Summary Statistics:" in call for call in calls))
    
    @patch('builtins.print')
    @patch('main.sales_data_generator')
    def test_summarize_sales_custom_params(self, mock_generator, mock_print):
        """Test sales summary with custom parameters."""
        mock_generator.return_value = [[100.0]]
        
        summarize_sales(1, seed=123)
        
        mock_generator.assert_called_once_with(1, 123)
    
    def test_summarize_sales_invalid_customers(self):
        """Test summarize_sales with invalid customer counts."""
        with self.assertRaises(ValueError):
            summarize_sales(0)
        
        with self.assertRaises(ValueError):
            summarize_sales(-5)
        
        with self.assertRaises(ValueError):
            summarize_sales(1001)
    
    @patch('builtins.print')
    @patch('main.sales_data_generator')
    def test_summarize_sales_statistics(self, mock_generator, mock_print):
        """Test that summary statistics are calculated correctly."""
        mock_generator.return_value = [
            [10.0, 20.0],  # Customer 1: $30.00
            [5.0],         # Customer 2: $5.00
            [15.0, 25.0, 35.0]  # Customer 3: $75.00
        ]
        
        summarize_sales(3, seed=42)
        
        # Check that statistics are printed
        calls = [str(call) for call in mock_print.call_args_list]
        output_text = ' '.join(calls)
        
        self.assertIn("Total customers: 3", output_text)
        self.assertIn("Total purchases: 6", output_text)
        self.assertIn("Total revenue: $110.00", output_text)
        self.assertIn("Average per customer: $36.67", output_text)
        self.assertIn("Average per purchase: $18.33", output_text)


if __name__ == "__main__":
    unittest.main()