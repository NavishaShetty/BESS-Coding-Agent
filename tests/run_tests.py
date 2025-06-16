import pytest
import sys
import os

def run_tests():
    # Get the directory containing this script
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the parent directory to Python path
    parent_dir = os.path.dirname(tests_dir)
    sys.path.append(parent_dir)
    
    # Run pytest on the test directory
    pytest.main([tests_dir])

if __name__ == '__main__':
    run_tests()