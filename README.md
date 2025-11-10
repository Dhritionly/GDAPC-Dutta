# GDAPC-Dutta Data Projects

This repository collects practice materials for the Google Data Analytics
Professional Certificate. It includes a small Python package for exploring EPA
air-quality data as well as supporting artefacts for the Automatidata capstone
project. The codebase now provides a lightweight command-line script, comprehensive
utility functions, and robust error handling for data analysis workflows.

## 🚀 Features

- **EPA Air Quality Analysis**: Load and analyze EPA air quality data with built-in validation
- **Synthetic Data Generation**: Generate realistic sales data and customer identifiers for testing
- **Comprehensive Error Handling**: Robust error handling with detailed logging throughout
- **Input Validation**: Extensive input validation for all functions to prevent runtime errors
- **Logging Utilities**: Configurable logging system for debugging and monitoring
- **Test Suite**: Comprehensive unit tests covering all major functionality
- **Example Scripts**: Detailed examples showing how to use each component
- **Configuration Management**: Environment-based configuration for different deployment scenarios

## 📁 Repository structure

```
.
├── AirQuality_Analysis/
│   ├── ada_c2_labs.py          # Enhanced helper functions for EPA data labs
│   ├── c2_epa_air_quality.csv  # EPA air-quality sample dataset
│   └── Activity_ ... .ipynb    # Course notebooks
├── Automatidata Project/        # Reference documents and datasets
├── utils/                       # Utility modules
│   ├── __init__.py             # Package initialization
│   ├── logging_utils.py        # Logging configuration and utilities
│   └── validation.py           # Input validation functions
├── tests/                       # Test suite
│   ├── __init__.py             # Test runner
│   ├── test_ada_c2_labs.py    # Tests for EPA data functions
│   ├── test_main.py            # Tests for main module
│   ├── test_logging_utils.py   # Tests for logging utilities
│   └── test_validation.py      # Tests for validation functions
├── examples/                    # Example usage scripts
│   ├── epa_analysis_example.py # EPA data analysis examples
│   ├── sales_analysis_example.py # Sales data generation examples
│   └── validation_examples.py  # Input validation examples
├── main.py                     # Enhanced command-line entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── Makefile                    # Development tasks and commands
└── README.md                   # Project documentation (this file)
```

## 🛠️ Installation

### Prerequisites

- Python 3.10 or newer
- `pip` for managing Python packages

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd GDAPC-Dutta

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python main.py
```

### Development Setup

For development with additional tools:

```bash
# Set up development environment
make setup-dev

# Or manually install dev dependencies
pip install pytest pytest-cov black flake8 mypy
```

## 📖 Usage

### Basic Demo

Run the main demo script to preview the available utilities and datasets:

```bash
python main.py
```

Example output:

```
Hi, GDAPC community!
EPA Air Quality sample:
  - Alabama, Jefferson: AQI 48
  - Alabama, Jefferson: AQI 55
  - ...
Synthetic sales summary:
  - Customer 1: 2 purchases, total $74.10 ($32.12, $41.98)
  - ...

Summary Statistics:
  - Total customers: 3
  - Total purchases: 6
  - Total revenue: $156.78
  - Average per customer: $52.26
  - Average per purchase: $26.13
```

### Using the Helper Functions

```python
from AirQuality_Analysis.ada_c2_labs import fetch_epa, lists_gen, sales_data_generator

# Load EPA data
states = fetch_epa("state")
counties = fetch_epa("county")
aqi_values = fetch_epa("aqi")

# Generate sample IDs for tracking
verified_ids, feedback_ids = lists_gen(
    n_chars_id=8,
    n_pool=1000,
    n_feedback_ids=50,
    n_verified_ids=75,
    seed=42
)

# Generate synthetic sales data
sales_data = sales_data_generator(n_customers=100, seed=123)
```

### Advanced Usage with Custom Configuration

```python
from utils.logging_utils import setup_logger
from config import get_config

# Set up custom logging
logger = setup_logger(
    "my_app",
    level="DEBUG",
    log_file="my_analysis.log"
)

# Access configuration
config = get_config()
print(f"Data directory: {config.data_dir}")
print(f"Max batch size: {config.max_records_per_batch}")
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific test file
python -m pytest tests/test_ada_c2_labs.py -v
```

### Test Coverage

The test suite covers:
- All core functions in `ada_c2_labs.py`
- Main module functionality
- Validation utilities
- Logging utilities
- Error handling scenarios

## 📝 Examples

The `examples/` directory contains comprehensive usage examples:

### EPA Air Quality Analysis

```bash
python examples/epa_analysis_example.py
```

Demonstrates:
- Loading and analyzing EPA data
- Statistical analysis of air quality
- Custom data file processing
- ID generation for data tracking

### Sales Data Analysis

```bash
python examples/sales_analysis_example.py
```

Demonstrates:
- Synthetic sales data generation
- Customer behavior analysis
- Performance benchmarking
- Revenue analysis

### Input Validation

```bash
python examples/validation_examples.py
```

Demonstrates:
- File path validation
- Numeric input validation
- Parameter range checking
- Error handling patterns

## 🔧 Development

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Run all quality checks
make check-all
```

### Development Workflow

```bash
# Quick development cycle (format, test, run)
make dev-cycle

# Run all examples
make run-examples

# Clean temporary files
make clean
```

### Configuration

The project supports environment-based configuration:

```bash
# Set custom data directory
export GDAPC_DATA_DIR=/path/to/data

# Set logging level
export GDAPC_LOG_LEVEL=DEBUG

# Set environment
export GDAPC_ENV=production

# View current configuration
python config.py
```

## 📊 API Reference

### Core Functions

#### `fetch_epa(key, csv_path=None)`
Load EPA air quality data from CSV files.

**Parameters:**
- `key`: One of "state", "county", or "aqi"
- `csv_path`: Optional custom CSV file path

**Returns:** List of values for the specified column

**Raises:** `ValueError`, `FileNotFoundError`, `pd.errors.EmptyDataError`

#### `sales_data_generator(n_customers, seed)`
Generate synthetic sales data for testing.

**Parameters:**
- `n_customers`: Number of customers to simulate (1-1000)
- `seed`: Random seed for reproducible results

**Returns:** List of customer sales histories

#### `lists_gen(n_chars_id, n_pool, n_feedback_ids, n_verified_ids, seed=None)`
Generate sample ID lists for tracking.

**Parameters:**
- `n_chars_id`: Length of each identifier
- `n_pool`: Total pool size to sample from
- `n_feedback_ids`: Number of feedback IDs
- `n_verified_ids`: Number of verified IDs
- `seed`: Optional random seed

**Returns:** Tuple of (verified_ids, feedback_ids)

### Validation Functions

#### `validate_positive_int(value, param_name, allow_zero=False)`
Validate that a value is a positive integer.

#### `validate_range(value, param_name, min_val=None, max_val=None)`
Validate that a value is within a specified range.

#### `validate_file_path(file_path, must_exist=True, expected_extensions=None)`
Validate file paths and extensions.

## 🐛 Error Handling

The project includes comprehensive error handling:

- **Input Validation**: All functions validate inputs before processing
- **File Operations**: Robust handling of missing files and invalid formats
- **Memory Management**: Protection against excessive memory usage
- **Logging**: Detailed error logging for debugging
- **Graceful Degradation**: Informative error messages for users

## 📋 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GDAPC_DATA_DIR` | `./data` | Directory for data files |
| `GDAPC_OUTPUT_DIR` | `./output` | Directory for output files |
| `GDAPC_LOG_DIR` | `./logs` | Directory for log files |
| `GDAPC_LOG_LEVEL` | `INFO` | Logging level |
| `GDAPC_MAX_RECORDS_PER_BATCH` | `10000` | Maximum records per batch |
| `GDAPC_STRICT_VALIDATION` | `true` | Enable strict input validation |
| `GDAPC_ENV` | `development` | Environment (development/production) |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper testing
4. Run quality checks (`make check-all`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow Python best practices and PEP 8
- Add type hints to all functions
- Include comprehensive docstrings
- Write tests for new functionality
- Run `make format` before committing
- Ensure all tests pass (`make test`)

## 📄 License

This project is part of the Google Data Analytics Professional Certificate learning materials.

## 🙏 Acknowledgments

- Google Data Analytics Professional Certificate program
- U.S. Environmental Protection Agency (EPA) for air quality data
- Python data science community for tools and best practices

## 📞 Support

For issues, questions, or contributions:

1. Check the examples directory for usage patterns
2. Review the test files for implementation details
3. Check existing issues or create a new one
4. Run `make help` for available commands

---

**Note**: This project is designed for educational purposes and demonstrates best practices in data analysis, error handling, and software development.
