"""Configuration management for the GDAPC-Dutta data analysis project."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from utils.logging_utils import get_logger
from utils.validation import validate_directory_path, validate_range

# Initialize logger
logger = get_logger(__name__)


class Config:
    """Configuration class for the GDAPC-Dutta project.
    
    This class manages configuration settings from environment variables
    and provides sensible defaults for development and production use.
    """
    
    def __init__(self):
        """Initialize configuration with default values and environment overrides."""
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables."""
        # Data paths
        self.data_dir = Path(
            os.getenv("GDAPC_DATA_DIR", 
                     Path(__file__).parent.parent / "data")
        )
        
        self.output_dir = Path(
            os.getenv("GDAPC_OUTPUT_DIR", 
                     Path(__file__).parent.parent / "output")
        )
        
        self.log_dir = Path(
            os.getenv("GDAPC_LOG_DIR", 
                     Path(__file__).parent.parent / "logs")
        )
        
        # Logging configuration
        self.log_level = os.getenv("GDAPC_LOG_LEVEL", "INFO")
        self.log_format = os.getenv(
            "GDAPC_LOG_FORMAT",
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        
        # Data processing limits
        self.max_records_per_batch = int(
            os.getenv("GDAPC_MAX_RECORDS_PER_BATCH", "10000")
        )
        
        self.max_file_size_mb = int(
            os.getenv("GDAPC_MAX_FILE_SIZE_MB", "100")
        )
        
        # Performance settings
        self.enable_caching = os.getenv("GDAPC_ENABLE_CACHING", "true").lower() == "true"
        self.cache_ttl_seconds = int(
            os.getenv("GDAPC_CACHE_TTL_SECONDS", "3600")
        )
        
        # Validation settings
        self.strict_validation = os.getenv("GDAPC_STRICT_VALIDATION", "true").lower() == "true"
        
        # Apply validation
        self._validate_config()
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _validate_config(self):
        """Validate configuration values."""
        try:
            # Validate numeric ranges
            validate_range(self.max_records_per_batch, "max_records_per_batch", min_val=1, max_val=1000000)
            validate_range(self.max_file_size_mb, "max_file_size_mb", min_val=1, max_val=10000)
            validate_range(self.cache_ttl_seconds, "cache_ttl_seconds", min_val=0)
            
            logger.debug("Configuration validation passed")
            
        except ValueError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        try:
            # Create directories if they don't exist
            self.data_dir = validate_directory_path(
                self.data_dir, must_exist=False, create_if_missing=True
            )
            
            self.output_dir = validate_directory_path(
                self.output_dir, must_exist=False, create_if_missing=True
            )
            
            self.log_dir = validate_directory_path(
                self.log_dir, must_exist=False, create_if_missing=True
            )
            
            logger.debug(f"Ensured directories exist: {self.data_dir}, {self.output_dir}, {self.log_dir}")
            
        except OSError as e:
            logger.error(f"Failed to create directories: {e}")
            raise
    
    def get_epa_data_path(self) -> Path:
        """Get the default EPA data file path.
        
        Returns:
            Path to the EPA air quality CSV file.
        """
        return Path(__file__).parent.parent / "AirQuality_Analysis" / "c2_epa_air_quality.csv"
    
    def get_default_log_file(self) -> Path:
        """Get the default log file path.
        
        Returns:
            Path to the default log file.
        """
        return self.log_dir / "gdapc.log"
    
    def is_development(self) -> bool:
        """Check if running in development mode.
        
        Returns:
            True if in development mode, False otherwise.
        """
        return os.getenv("GDAPC_ENV", "development").lower() == "development"
    
    def is_production(self) -> bool:
        """Check if running in production mode.
        
        Returns:
            True if in production mode, False otherwise.
        """
        return os.getenv("GDAPC_ENV", "development").lower() == "production"
    
    def __str__(self) -> str:
        """Return string representation of configuration."""
        return (
            f"Config(\n"
            f"  data_dir={self.data_dir},\n"
            f"  output_dir={self.output_dir},\n"
            f"  log_dir={self.log_dir},\n"
            f"  log_level={self.log_level},\n"
            f"  max_records_per_batch={self.max_records_per_batch},\n"
            f"  max_file_size_mb={self.max_file_size_mb},\n"
            f"  enable_caching={self.enable_caching},\n"
            f"  strict_validation={self.strict_validation},\n"
            f"  environment={os.getenv('GDAPC_ENV', 'development')}\n"
            f")"
        )


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance.
    
    Returns:
        The global Config instance.
    """
    return config


def reload_config():
    """Reload the configuration from environment variables.
    
    This is useful for testing or when environment variables change
    during runtime.
    """
    global config
    config = Config()
    logger.info("Configuration reloaded")


if __name__ == "__main__":
    # Print current configuration
    print("Current GDAPC-Dutta Configuration:")
    print(config)