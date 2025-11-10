"""Test suite for logging utilities."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from utils.logging_utils import setup_logger, get_logger, log_function_call


class TestSetupLogger(unittest.TestCase):
    """Test cases for setup_logger function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.log_file = self.temp_dir / "test.log"
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.log_file.exists():
            self.log_file.unlink()
        self.temp_dir.rmdir()
    
    def test_setup_logger_console_only(self):
        """Test logger setup with console output only."""
        logger = setup_logger("test_logger", level="INFO")
        
        self.assertEqual(logger.name, "test_logger")
        self.assertEqual(logger.level, 20)  # INFO level
        self.assertEqual(len(logger.handlers), 1)  # Only console handler
    
    def test_setup_logger_with_file(self):
        """Test logger setup with file output."""
        logger = setup_logger(
            "test_logger_file", 
            level="DEBUG", 
            log_file=self.log_file
        )
        
        self.assertEqual(len(logger.handlers), 2)  # Console + file handlers
        self.assertTrue(self.log_file.exists())
    
    def test_setup_logger_invalid_level(self):
        """Test logger setup with invalid level."""
        with self.assertRaises(ValueError):
            setup_logger("test_logger", level="INVALID")
    
    def test_setup_logger_custom_format(self):
        """Test logger setup with custom format."""
        custom_format = "%(levelname)s - %(message)s"
        logger = setup_logger(
            "test_logger_format", 
            format_string=custom_format
        )
        
        # Check that handlers use the custom format
        for handler in logger.handlers:
            self.assertEqual(handler.formatter._fmt, custom_format)
    
    def test_setup_logger_file_creation_error(self):
        """Test logger setup with file creation error."""
        invalid_path = Path("/invalid/path/that/does/not/exist/test.log")
        
        with self.assertRaises(OSError):
            setup_logger("test_logger_error", log_file=invalid_path)


class TestGetLogger(unittest.TestCase):
    """Test cases for get_logger function."""
    
    def test_get_logger_default(self):
        """Test getting logger with default configuration."""
        logger = get_logger("test_default")
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, 20)  # INFO level
        self.assertEqual(len(logger.handlers), 1)  # Console handler


class TestLogFunctionCall(unittest.TestCase):
    """Test cases for log_function_call function."""
    
    @patch('utils.logging_utils.get_logger')
    def test_log_function_call_basic(self, mock_get_logger):
        """Test basic function call logging."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        log_function_call("test_func", (1, 2), {"param": "value"})
        
        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0][0]
        self.assertIn("test_func", call_args)
        self.assertIn("1", call_args)
        self.assertIn("2", call_args)
        self.assertIn("param=value", call_args)
    
    @patch('utils.logging_utils.get_logger')
    def test_log_function_call_long_string(self, mock_get_logger):
        """Test function call logging with long string."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        long_string = "a" * 150  # String longer than 100 characters
        log_function_call("test_func", (long_string,), {})
        
        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0][0]
        self.assertIn("aaa...", call_args)  # Should be truncated
    
    @patch('utils.logging_utils.get_logger')
    def test_log_function_call_long_list(self, mock_get_logger):
        """Test function call logging with long list."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        long_list = list(range(10))  # List longer than 5 elements
        log_function_call("test_func", (long_list,), {})
        
        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0][0]
        self.assertIn("list(length=10)", call_args)  # Should show length


if __name__ == "__main__":
    unittest.main()