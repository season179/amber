"""
Setup script for Amber.txt
"""
from setuptools import setup, find_packages

setup(
    name="amber-txt",
    version="0.1.0",
    description="Agent-based personal AI assistant with plain text memory storage",
    author="Amber.txt Team",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.25.0",
        "openai>=1.0.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "langchain>=0.0.267",
        "litellm>=0.10.0",
        "openrouter>=0.1.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "amber=app:main",
        ],
    },
)