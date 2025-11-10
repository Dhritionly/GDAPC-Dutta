"""Utility functions used throughout the air quality analysis labs.

This module provides functions for loading and processing EPA air quality data,
generating synthetic identifiers, and creating simulated sales data for analysis
purposes.
"""

from __future__ import annotations

import random
import string
from pathlib import Path
from typing import Any, Literal

import pandas as pd

from utils.logging_utils import get_logger, log_function_call
from utils.validation import (
    validate_file_path,
    validate_literal,
    validate_positive_int,
    validate_range,
    validate_seed,
)

EPAKey = Literal["state", "county", "aqi"]
ALPHANUMERIC = string.ascii_lowercase + string.digits

# Initialize logger
logger = get_logger(__name__)

# Default path for EPA data
DEFAULT_EPA_DATA_PATH = Path(__file__).parent / "c2_epa_air_quality.csv"


def fetch_epa(key: EPAKey, csv_path: str | Path = DEFAULT_EPA_DATA_PATH) -> list[Any]:
    """Return a column from the EPA air quality dataset.

    Args:
        key: One of ``"state"``, ``"county"`` or ``"aqi"`` identifying the
            column to read from the dataset.
        csv_path: Path to the EPA CSV data file. Defaults to the included
            c2_epa_air_quality.csv file.

    Returns:
        A list containing the requested column values.

    Raises:
        KeyError: If ``key`` is not recognised.
        FileNotFoundError: If the CSV file is not found.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file cannot be parsed.
        ValueError: If required columns are missing from the dataset.
    """
    log_function_call("fetch_epa", (key,), {"csv_path": csv_path})
    
    # Validate inputs
    validate_literal(key, ["state", "county", "aqi"], "key")
    validated_path = validate_file_path(
        csv_path, must_exist=True, expected_extensions=[".csv"]
    )
    
    try:
        logger.debug(f"Loading EPA data from {validated_path}")
        epa = pd.read_csv(validated_path)
        
        # Check if dataframe is empty
        if epa.empty:
            raise pd.errors.EmptyDataError("CSV file is empty")
        
        # Validate required columns exist
        column_mapping = {
            "state": "state_name",
            "county": "county_name", 
            "aqi": "aqi"
        }
        
        required_column = column_mapping[key]
        if required_column not in epa.columns:
            available_columns = list(epa.columns)
            raise ValueError(
                f"Column '{required_column}' not found in dataset. "
                f"Available columns: {available_columns}"
            )
        
        # Extract and return the data
        result = epa[required_column].tolist()
        logger.debug(f"Successfully extracted {len(result)} values for '{key}'")
        return result
        
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty CSV file: {validated_path}")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"Failed to parse CSV file {validated_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading EPA data: {e}")
        raise


def id_gen(n_chars_id: int, n_samples: int) -> list[str]:
    """Generate deterministic random-looking identifiers.

    Args:
        n_chars_id: Number of characters each identifier should contain.
            Must be a positive integer.
        n_samples: Number of identifiers to generate.
            Must be a positive integer.

    Returns:
        A list of alphanumeric identifier strings.

    Raises:
        ValueError: If n_chars_id or n_samples are not positive integers.
        MemoryError: If n_samples is too large for available memory.
    """
    log_function_call("id_gen", (n_chars_id, n_samples), {})
    
    # Validate inputs
    validate_positive_int(n_chars_id, "n_chars_id")
    validate_positive_int(n_samples, "n_samples")
    
    # Check for reasonable limits to prevent memory issues
    if n_samples > 1000000:
        raise MemoryError(
            f"Requested {n_samples} identifiers, which may cause memory issues. "
            "Please use a smaller number or process in batches."
        )
    
    if n_chars_id > 100:
        raise ValueError(
            f"Identifier length {n_chars_id} is too long. "
            "Maximum recommended length is 100 characters."
        )
    
    try:
        logger.debug(f"Generating {n_samples} identifiers with {n_chars_id} characters each")
        result = [
            "".join(random.Random(index).choices(ALPHANUMERIC, k=n_chars_id))
            for index in range(n_samples)
        ]
        logger.debug(f"Successfully generated {len(result)} identifiers")
        return result
    except Exception as e:
        logger.error(f"Error generating identifiers: {e}")
        raise


def lists_gen(
    n_chars_id: int,
    n_pool: int,
    n_feedback_ids: int,
    n_verified_ids: int,
    seed: int | None = None,
) -> tuple[list[str], list[str]]:
    """Return two ID subsets representing verified and feedback IDs.

    Args:
        n_chars_id: Length of each generated identifier.
            Must be a positive integer.
        n_pool: Size of the ID pool to sample from.
            Must be a positive integer.
        n_feedback_ids: Number of IDs assigned to the feedback list.
            Must be a non-negative integer.
        n_verified_ids: Number of IDs assigned to the verified list.
            Must be a non-negative integer.
        seed: Optional seed value to make sampling reproducible.

    Returns:
        A tuple containing the verified IDs and feedback IDs in that order.

    Raises:
        ValueError: If pool size is too small for requested sample sizes,
            or if any parameter is invalid.
        MemoryError: If n_pool is too large for available memory.
    """
    log_function_call(
        "lists_gen",
        (n_chars_id, n_pool, n_feedback_ids, n_verified_ids),
        {"seed": seed}
    )
    
    # Validate inputs
    validate_positive_int(n_chars_id, "n_chars_id")
    validate_positive_int(n_pool, "n_pool")
    validate_positive_int(n_feedback_ids, "n_feedback_ids", allow_zero=True)
    validate_positive_int(n_verified_ids, "n_verified_ids", allow_zero=True)
    validate_seed(seed)
    
    # Validate pool size is sufficient
    max_sample_size = max(n_feedback_ids, n_verified_ids)
    if n_pool < max_sample_size:
        raise ValueError(
            f"Pool size ({n_pool}) must be at least as large as the largest "
            f"sample size ({max_sample_size})."
        )
    
    # Check if we have enough unique IDs for both lists
    total_required = n_feedback_ids + n_verified_ids
    if total_required > n_pool:
        raise ValueError(
            f"Pool size ({n_pool}) is too small for both feedback ({n_feedback_ids}) "
            f"and verified ({n_verified_ids}) IDs. Total required: {total_required}"
        )

    try:
        logger.debug(f"Generating ID pool of size {n_pool}")
        pool = id_gen(n_chars_id, n_pool)
        
        rng = random.Random(seed)
        
        logger.debug(f"Sampling {n_verified_ids} verified IDs")
        verified_ids = rng.sample(pool, k=n_verified_ids)
        
        logger.debug(f"Sampling {n_feedback_ids} feedback IDs")
        feedback_ids = rng.sample(pool, k=n_feedback_ids)
        
        logger.debug(f"Successfully generated ID lists: {len(verified_ids)} verified, {len(feedback_ids)} feedback")
        return verified_ids, feedback_ids
        
    except ValueError as e:
        logger.error(f"Error in lists_gen: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in lists_gen: {e}")
        raise


def sales_data_generator(n_customers: int, seed: int) -> list[list[float]]:
    """Create simulated sales histories for a set of customers.

    Args:
        n_customers: Number of customers to simulate.
            Must be a positive integer.
        seed: Seed value for deterministic random number generation.
            Must be an integer.

    Returns:
        A nested list where each inner list contains the purchases for a
        customer. Individual purchase amounts are rounded to two decimals.
        Each inner list may be empty if a customer has no purchases.

    Raises:
        ValueError: If n_customers is not a positive integer.
        TypeError: If seed is not an integer.
        MemoryError: If n_customers is too large for available memory.
    """
    log_function_call("sales_data_generator", (n_customers,), {"seed": seed})
    
    # Validate inputs
    validate_positive_int(n_customers, "n_customers")
    validate_seed(seed)
    
    # Check for reasonable limits
    if n_customers > 1000000:
        raise MemoryError(
            f"Requested {n_customers} customers, which may cause memory issues. "
            "Please use a smaller number or process in batches."
        )
    
    try:
        rng = random.Random(seed)
        sales_data: list[list[float]] = []
        
        logger.debug(f"Generating sales data for {n_customers} customers")
        
        for customer_idx in range(n_customers):
            # Generate 0-6 sales per customer
            n_sales = rng.randint(0, 6)
            
            customer_sales = [
                round(rng.lognormvariate(2.5, 1.5), 2) for _ in range(n_sales)
            ]
            
            sales_data.append(customer_sales)
            
            # Log progress for large datasets
            if n_customers > 10000 and customer_idx % 10000 == 0:
                logger.debug(f"Processed {customer_idx}/{n_customers} customers")
        
        total_sales = sum(len(customer) for customer in sales_data)
        logger.debug(f"Generated sales data: {total_sales} total sales across {n_customers} customers")
        
        return sales_data
        
    except Exception as e:
        logger.error(f"Error generating sales data: {e}")
        raise
