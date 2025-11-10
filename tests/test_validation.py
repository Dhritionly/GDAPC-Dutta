"""Test suite for utility modules."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from utils.validation import (
    validate_file_path,
    validate_positive_int,
    validate_range,
    validate_literal,
    validate_seed,
    validate_directory_path,
)


class TestValidateFilePath(unittest.TestCase):
    """Test cases for validate_file_path function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.temp_file = self.temp_dir / "test.txt"
        self.temp_file.write_text("test content")
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_file.unlink()
        self.temp_dir.rmdir()
    
    def test_validate_file_path_exists(self):
        """Test validation of existing file."""
        result = validate_file_path(self.temp_file, must_exist=True)
        self.assertEqual(result, self.temp_file)
    
    def test_validate_file_path_not_exists_must_exist(self):
        """Test validation of non-existent file when must_exist=True."""
        with self.assertRaises(FileNotFoundError):
            validate_file_path(self.temp_dir / "nonexistent.txt", must_exist=True)
    
    def test_validate_file_path_not_exists_not_required(self):
        """Test validation of non-existent file when must_exist=False."""
        result = validate_file_path(self.temp_dir / "nonexistent.txt", must_exist=False)
        self.assertEqual(result, self.temp_dir / "nonexistent.txt")
    
    def test_validate_file_path_extension(self):
        """Test validation with allowed extensions."""
        result = validate_file_path(
            self.temp_file, must_exist=True, expected_extensions=[".txt", ".csv"]
        )
        self.assertEqual(result, self.temp_file)
    
    def test_validate_file_path_invalid_extension(self):
        """Test validation with disallowed extension."""
        with self.assertRaises(ValueError):
            validate_file_path(
                self.temp_file, must_exist=True, expected_extensions=[".csv", ".json"]
            )
    
    def test_validate_file_path_invalid_type(self):
        """Test validation with invalid path type."""
        with self.assertRaises(TypeError):
            validate_file_path(123)


class TestValidatePositiveInt(unittest.TestCase):
    """Test cases for validate_positive_int function."""
    
    def test_validate_positive_int_valid(self):
        """Test validation of positive integers."""
        result = validate_positive_int(5)
        self.assertEqual(result, 5)
    
    def test_validate_positive_int_zero_not_allowed(self):
        """Test validation of zero when not allowed."""
        with self.assertRaises(ValueError):
            validate_positive_int(0)
    
    def test_validate_positive_int_zero_allowed(self):
        """Test validation of zero when allowed."""
        result = validate_positive_int(0, allow_zero=True)
        self.assertEqual(result, 0)
    
    def test_validate_positive_int_negative(self):
        """Test validation of negative integers."""
        with self.assertRaises(ValueError):
            validate_positive_int(-5)
    
    def test_validate_positive_int_invalid_type(self):
        """Test validation with invalid type."""
        with self.assertRaises(TypeError):
            validate_positive_int("5")


class TestValidateRange(unittest.TestCase):
    """Test cases for validate_range function."""
    
    def test_validate_range_valid(self):
        """Test validation of value in range."""
        result = validate_range(5, min_val=1, max_val=10)
        self.assertEqual(result, 5)
    
    def test_validate_range_below_min(self):
        """Test validation of value below minimum."""
        with self.assertRaises(ValueError):
            validate_range(0, min_val=1, max_val=10)
    
    def test_validate_range_above_max(self):
        """Test validation of value above maximum."""
        with self.assertRaises(ValueError):
            validate_range(11, min_val=1, max_val=10)
    
    def test_validate_range_no_bounds(self):
        """Test validation with no bounds."""
        result = validate_range(5)
        self.assertEqual(result, 5)
    
    def test_validate_range_only_min(self):
        """Test validation with only minimum bound."""
        result = validate_range(10, min_val=5)
        self.assertEqual(result, 10)
    
    def test_validate_range_only_max(self):
        """Test validation with only maximum bound."""
        result = validate_range(3, max_val=10)
        self.assertEqual(result, 3)
    
    def test_validate_range_invalid_type(self):
        """Test validation with invalid type."""
        with self.assertRaises(TypeError):
            validate_range("5", min_val=1, max_val=10)


class TestValidateLiteral(unittest.TestCase):
    """Test cases for validate_literal function."""
    
    def test_validate_literal_valid(self):
        """Test validation of valid literal."""
        result = validate_literal("red", ["red", "green", "blue"])
        self.assertEqual(result, "red")
    
    def test_validate_literal_invalid(self):
        """Test validation of invalid literal."""
        with self.assertRaises(ValueError):
            validate_literal("yellow", ["red", "green", "blue"])
    
    def test_validate_literal_empty_list(self):
        """Test validation with empty valid values list."""
        with self.assertRaises(ValueError):
            validate_literal("anything", [])


class TestValidateSeed(unittest.TestCase):
    """Test cases for validate_seed function."""
    
    def test_validate_seed_none(self):
        """Test validation of None seed."""
        result = validate_seed(None)
        self.assertIsNone(result)
    
    def test_validate_seed_int(self):
        """Test validation of integer seed."""
        result = validate_seed(42)
        self.assertEqual(result, 42)
    
    def test_validate_seed_invalid_type(self):
        """Test validation with invalid seed type."""
        with self.assertRaises(TypeError):
            validate_seed("42")


class TestValidateDirectoryPath(unittest.TestCase):
    """Test cases for validate_directory_path function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.temp_file = self.temp_dir / "test.txt"
        self.temp_file.write_text("test content")
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_file.unlink()
        self.temp_dir.rmdir()
    
    def test_validate_directory_path_exists(self):
        """Test validation of existing directory."""
        result = validate_directory_path(self.temp_dir, must_exist=True)
        self.assertEqual(result, self.temp_dir)
    
    def test_validate_directory_path_not_exists_must_exist(self):
        """Test validation of non-existent directory when must_exist=True."""
        with self.assertRaises(FileNotFoundError):
            validate_directory_path(self.temp_dir / "nonexistent", must_exist=True)
    
    def test_validate_directory_path_not_exists_create(self):
        """Test validation of non-existent directory with create_if_missing=True."""
        new_dir = self.temp_dir / "new_dir"
        result = validate_directory_path(new_dir, must_exist=False, create_if_missing=True)
        self.assertEqual(result, new_dir)
        self.assertTrue(new_dir.exists())
        self.assertTrue(new_dir.is_dir())
        new_dir.rmdir()
    
    def test_validate_directory_path_is_file(self):
        """Test validation when path exists but is a file."""
        with self.assertRaises(NotADirectoryError):
            validate_directory_path(self.temp_file, must_exist=True)
    
    def test_validate_directory_path_invalid_type(self):
        """Test validation with invalid path type."""
        with self.assertRaises(TypeError):
            validate_directory_path(123)


if __name__ == "__main__":
    unittest.main()