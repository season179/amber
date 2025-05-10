"""
Entry point for Amber.txt application
"""
import sys
import os

# Add the project directory to the Python path if needed
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Import and run the Streamlit app
from src.interface.app import main

if __name__ == "__main__":
    main()