"""Test runner for the GDAPC-Dutta project."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import all test modules
from tests.test_ada_c2_labs import *
from tests.test_main import *
from tests.test_validation import *
from tests.test_logging_utils import *


if __name__ == "__main__":
    # Create a test suite with all tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases from all modules
    test_modules = [
        "tests.test_ada_c2_labs",
        "tests.test_main", 
        "tests.test_validation",
        "tests.test_logging_utils"
    ]
    
    for module_name in test_modules:
        try:
            suite.addTests(loader.loadTestsFromName(module_name))
        except Exception as e:
            print(f"Failed to load tests from {module_name}: {e}")
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)