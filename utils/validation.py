"""Input validation utilities for data analysis functions."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal, Union


def validate_file_path(
    file_path: Union[str, Path],
    must_exist: bool = True,
    expected_extensions: Optional[list[str]] = None,
) -> Path:
    """Validate a file path.
    
    Args:
        file_path: Path to validate.
        must_exist: Whether the file must exist.
        expected_extensions: List of allowed file extensions (e.g., ['.csv', '.json']).
        
    Returns:
        Validated Path object.
        
    Raises:
        FileNotFoundError: If file must exist but doesn't.
        ValueError: If file extension is not in expected_extensions.
        TypeError: If file_path is not a string or Path.
    """
    if not isinstance(file_path, (str, Path)):
        raise TypeError(f"file_path must be str or Path, got {type(file_path)}")
    
    path = Path(file_path)
    
    if must_exist and not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if must_exist and not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    if expected_extensions:
        ext = path.suffix.lower()
        if ext not in [e.lower() for e in expected_extensions]:
            raise ValueError(
                f"File extension {ext} not allowed. "
                f"Expected: {expected_extensions}"
            )
    
    return path


def validate_positive_int(
    value: int, param_name: str = "value", allow_zero: bool = False
) -> int:
    """Validate that a value is a positive integer.
    
    Args:
        value: Value to validate.
        param_name: Name of the parameter for error messages.
        allow_zero: Whether zero is allowed.
        
    Returns:
        Validated integer value.
        
    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative or zero when not allowed.
    """
    if not isinstance(value, int):
        raise TypeError(f"{param_name} must be an integer, got {type(value)}")
    
    if allow_zero:
        if value < 0:
            raise ValueError(f"{param_name} must be non-negative, got {value}")
    else:
        if value <= 0:
            raise ValueError(f"{param_name} must be positive, got {value}")
    
    return value


def validate_range(
    value: Union[int, float],
    param_name: str = "value",
    min_val: Optional[Union[int, float]] = None,
    max_val: Optional[Union[int, float]] = None,
) -> Union[int, float]:
    """Validate that a value is within a specified range.
    
    Args:
        value: Value to validate.
        param_name: Name of the parameter for error messages.
        min_val: Minimum allowed value (inclusive).
        max_val: Maximum allowed value (inclusive).
        
    Returns:
        Validated value.
        
    Raises:
        TypeError: If value is not a number.
        ValueError: If value is outside the specified range.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{param_name} must be a number, got {type(value)}")
    
    if min_val is not None and value < min_val:
        raise ValueError(f"{param_name} must be >= {min_val}, got {value}")
    
    if max_val is not None and value > max_val:
        raise ValueError(f"{param_name} must be <= {max_val}, got {value}")
    
    return value


def validate_literal(value: Any, valid_values: list[Any], param_name: str = "value") -> Any:
    """Validate that a value is one of the allowed literal values.
    
    Args:
        value: Value to validate.
        valid_values: List of allowed values.
        param_name: Name of the parameter for error messages.
        
    Returns:
        Validated value.
        
    Raises:
        ValueError: If value is not in valid_values.
    """
    if value not in valid_values:
        raise ValueError(
            f"{param_name} must be one of {valid_values}, got {value}"
        )
    
    return value


def validate_seed(seed: Optional[int]) -> Optional[int]:
    """Validate a random seed value.
    
    Args:
        seed: Seed value to validate.
        
    Returns:
        Validated seed value.
        
    Raises:
        TypeError: If seed is not None or an integer.
    """
    if seed is not None and not isinstance(seed, int):
        raise TypeError(f"seed must be None or an integer, got {type(seed)}")
    
    return seed


def validate_directory_path(
    dir_path: Union[str, Path],
    must_exist: bool = True,
    create_if_missing: bool = False,
) -> Path:
    """Validate a directory path.
    
    Args:
        dir_path: Directory path to validate.
        must_exist: Whether the directory must exist.
        create_if_missing: Whether to create the directory if it doesn't exist.
        
    Returns:
        Validated Path object.
        
    Raises:
        FileNotFoundError: If directory must exist but doesn't.
        NotADirectoryError: If path exists but is not a directory.
        OSError: If directory creation fails.
    """
    if not isinstance(dir_path, (str, Path)):
        raise TypeError(f"dir_path must be str or Path, got {type(dir_path)}")
    
    path = Path(dir_path)
    
    if path.exists():
        if not path.is_dir():
            raise NotADirectoryError(f"Path exists but is not a directory: {path}")
    elif must_exist:
        raise FileNotFoundError(f"Directory not found: {path}")
    elif create_if_missing:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create directory {path}: {e}") from e
    
    return path