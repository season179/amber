#!/usr/bin/env python
"""
Test runner for Amber.txt
"""
import os
import sys
import unittest
import importlib
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def discover_and_run_tests(test_type=None):
    """
    Discover and run tests based on the test type.
    
    Args:
        test_type: Type of tests to run ('memory', 'agents', 'integration', or None for all)
    """
    if test_type and test_type not in ['memory', 'agents', 'integration']:
        print(f"Invalid test type: {test_type}")
        sys.exit(1)
    
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define test paths based on test type
    if test_type:
        test_paths = [os.path.join(test_dir, test_type)]
    else:
        test_paths = [
            os.path.join(test_dir, 'memory'),
            os.path.join(test_dir, 'agents'),
            os.path.join(test_dir, 'integration')
        ]
    
    # Discover and run test modules in each path
    for path in test_paths:
        print(f"\nRunning tests in {os.path.basename(path)} directory:")
        print("-" * 60)
        
        # Get all test files in the directory
        test_files = [f for f in os.listdir(path) 
                     if f.startswith('test_') and f.endswith('.py')]
        
        for test_file in test_files:
            # Convert file name to module name
            module_name = f"tests.{os.path.basename(path)}.{test_file[:-3]}"
            print(f"Running {test_file}...")
            
            try:
                # Import the module
                module = importlib.import_module(module_name)
                
                # Find test functions
                test_funcs = [attr for attr in dir(module) 
                             if attr.startswith('test_') and callable(getattr(module, attr))]
                
                # Run each test function
                for func_name in test_funcs:
                    test_func = getattr(module, func_name)
                    try:
                        test_func()
                        print(f"  ✓ {func_name}")
                    except Exception as e:
                        print(f"  ✗ {func_name} - {str(e)}")
                
            except Exception as e:
                print(f"Error running {test_file}: {str(e)}")
        
        print("-" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Amber.txt tests")
    parser.add_argument('--type', choices=['memory', 'agents', 'integration'],
                       help='Type of tests to run (memory, agents, integration, or all if not specified)')
    
    args = parser.parse_args()
    discover_and_run_tests(args.type)