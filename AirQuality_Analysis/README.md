# AirQuality_Analysis Module

A Python utility module for working with EPA air-quality data and generating synthetic IDs for data analysis exercises.

## Overview

This module provides helper functions originally designed for Coursera lab exercises. It has been enhanced with modern Python best practices while maintaining full backward compatibility with existing code.

## Features

- **EPA Data Loading**: Efficiently load and cache EPA air quality datasets
- **ID Generation**: Create deterministic synthetic IDs for testing and analysis
- **Sales Data Generation**: Generate realistic purchase histories using statistical distributions
- **Type Safety**: Full type hints for better IDE support and static analysis
- **Error Handling**: Comprehensive validation with clear, actionable error messages
- **Performance**: Optimized pandas operations with caching and efficient data types

## Functions

### `fetch_epa(key, csv_path=...)`

Return values for a requested EPA dataset column.

**Parameters:**
- `key` (str): One of "state", "county", or "aqi"
- `csv_path` (str | Path, optional): Path to the EPA dataset CSV file

**Returns:**
- `list[str | float]`: Column values

**Example:**
```python
from AirQuality_Analysis.ada_c2_labs import fetch_epa

states = fetch_epa("state")
counties = fetch_epa("county")
aqi_values = fetch_epa("aqi")
```

### `id_gen(n_chars_id, n_samples, *, seed=0, characters=None)`

Generate synthetic IDs comprised of lowercase letters and digits.

**Parameters:**
- `n_chars_id` (int): Number of characters per ID (must be > 0)
- `n_samples` (int): Number of IDs to generate (must be >= 0)
- `seed` (int | None, optional): Random seed for reproducibility (default: 0)
- `characters` (Sequence[str] | None, optional): Custom character pool

**Returns:**
- `list[str]`: Generated IDs

**Example:**
```python
from AirQuality_Analysis.ada_c2_labs import id_gen

# Generate 10 IDs, each 5 characters long
ids = id_gen(5, 10, seed=42)
# Result: ['3ql3g', 'dmcny', 'h8ue6', ...]
```

### `lists_gen(n_chars_id, n_pool, n_feedback_ids, n_verified_ids, *, seed=None)`

Create "feedback" and "verified" ID lists sampled from a shared pool.

**Parameters:**
- `n_chars_id` (int): Number of characters per ID
- `n_pool` (int): Size of the ID pool
- `n_feedback_ids` (int): Number of feedback IDs to sample
- `n_verified_ids` (int): Number of verified IDs to sample
- `seed` (int | None, optional): Random seed for reproducibility

**Returns:**
- `tuple[list[str], list[str]]`: (verified_ids, feedback_ids)

**Example:**
```python
from AirQuality_Analysis.ada_c2_labs import lists_gen

verified, feedback = lists_gen(5, 100, 20, 30, seed=42)
# verified contains 30 IDs, feedback contains 20 IDs
```

### `sales_data_generator(n_customers, seed=None)`

Generate synthetic purchase histories for multiple customers.

Each customer receives 0-6 purchases with values drawn from a log-normal distribution.

**Parameters:**
- `n_customers` (int): Number of customers (must be >= 0)
- `seed` (int | None, optional): Random seed for reproducibility

**Returns:**
- `list[list[float]]`: Nested list of sales amounts per customer

**Example:**
```python
from AirQuality_Analysis.ada_c2_labs import sales_data_generator

sales = sales_data_generator(100, seed=42)
# Result: [[12.34, 45.67], [8.90], [], ...]
# Each inner list represents purchases for one customer
```

## Improvements Made

### Code Quality
- ✅ Added comprehensive type hints to all functions and helpers
- ✅ Enhanced docstrings with numpy-style documentation
- ✅ Separated concerns with helper functions
- ✅ Added module-level documentation
- ✅ Defined `__all__` for explicit public API

### Error Handling
- ✅ Input validation with meaningful error messages
- ✅ Custom exception class for data loading errors
- ✅ Type checking for all parameters
- ✅ Range validation for numeric inputs
- ✅ File existence verification with helpful messages

### Performance Optimizations
- ✅ LRU caching for EPA dataset (avoids redundant disk I/O)
- ✅ Optimized pandas dtype usage (category, float32)
- ✅ Read only required columns from CSV
- ✅ Fixed inefficient seeding in `id_gen()`
- ✅ List comprehensions instead of append loops

### Code Structure
- ✅ Extracted constants to module level
- ✅ Used `pathlib.Path` for robust path handling
- ✅ Proper random number generator instances
- ✅ Consistent naming conventions
- ✅ PEP 8 compliant formatting

### Backward Compatibility
- ✅ All existing function signatures work unchanged
- ✅ Default parameters maintain original behavior
- ✅ Return types preserved
- ✅ Original use cases fully supported

## Dependencies

- Python 3.10+
- pandas
- numpy (transitive via pandas)

## Dataset

The module expects `c2_epa_air_quality.csv` in the same directory. The dataset contains:
- `state_name`: U.S. state names
- `county_name`: County names
- `aqi`: Air Quality Index values

## Error Messages

The module provides clear, actionable error messages:

```python
# Invalid key
fetch_epa("invalid")
# KeyError: Invalid key 'invalid'. Expected one of: aqi, county, state.

# Invalid n_chars_id
id_gen(0, 10)
# ValueError: n_chars_id must be at least 1, received 0.

# Pool too small
lists_gen(5, 10, 20, 5)
# ValueError: n_pool must be greater than or equal to both n_feedback_ids and n_verified_ids.
```

## Migration Guide

The enhanced module is fully backward compatible. Existing code will continue to work without changes:

```python
# Old code - still works!
states = fetch_epa("state")
ids = id_gen(5, 10)
verified, feedback = lists_gen(5, 100, 20, 30)
sales = sales_data_generator(100, 42)
```

New features can be adopted gradually:

```python
# New features available
from pathlib import Path

# Custom dataset path
states = fetch_epa("state", csv_path=Path("~/data/epa.csv"))

# Explicit seed control
ids = id_gen(5, 10, seed=None)  # Use system randomness

# Custom character pool
ids = id_gen(5, 10, characters="0123456789")  # Digits only
```

## License

This module is part of a data analysis training repository and is provided for educational purposes.
