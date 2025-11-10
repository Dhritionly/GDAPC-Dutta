"""Logging utilities for the GDAPC-Dutta data analysis project."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

from . import __version__


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str | Path] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """Set up a logger with console and optional file output.
    
    Args:
        name: Name of the logger (typically __name__).
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to a log file. If None, only console output.
        format_string: Custom format string for log messages.
        
    Returns:
        Configured logger instance.
        
    Raises:
        ValueError: If level is not a valid logging level.
        OSError: If log file cannot be created or written to.
    """
    # Validate logging level
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level.upper() not in valid_levels:
        raise ValueError(f"Invalid logging level: {level}. Must be one of {valid_levels}")
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Set default format if not provided
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file is not None:
        log_path = Path(log_file)
        try:
            # Create parent directories if they don't exist
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError as e:
            raise OSError(f"Failed to create log file {log_path}: {e}") from e
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with default configuration.
    
    Args:
        name: Name of the logger.
        
    Returns:
        Logger instance with default INFO level configuration.
    """
    return setup_logger(name, level="INFO")


def log_function_call(func_name: str, args: tuple, kwargs: dict) -> None:
    """Log a function call with its arguments.
    
    Args:
        func_name: Name of the function being called.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.
    """
    logger = get_logger(__name__)
    
    # Format arguments for logging (truncate long strings/lists)
    def format_arg(arg):
        if isinstance(arg, str) and len(arg) > 100:
            return f"{arg[:97]}..."
        elif isinstance(arg, (list, tuple)) and len(arg) > 5:
            return f"{type(arg).__name__}(length={len(arg)})"
        return str(arg)
    
    args_str = ", ".join(format_arg(arg) for arg in args)
    kwargs_str = ", ".join(f"{k}={format_arg(v)}" for k, v in kwargs.items())
    
    all_args = ", ".join(filter(None, [args_str, kwargs_str]))
    logger.debug(f"Calling {func_name}({all_args})")