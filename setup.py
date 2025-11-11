#!/usr/bin/env python3
"""
Setup script for travelpurpose package

This provides a fallback setup.py for better PyPI compatibility
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

# Read version from pyproject.toml
version = "0.2.0"

setup(
    name="travelpurpose",
    version=version,
    description="Production-grade library for classifying world cities by travel purpose using multi-source data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Travel Purpose Contributors",
    url="https://github.com/teyfikoz/Travel_Purpose-City_Tags",
    project_urls={
        "Homepage": "https://github.com/teyfikoz/Travel_Purpose-City_Tags",
        "Documentation": "https://github.com/teyfikoz/Travel_Purpose-City_Tags#readme",
        "Repository": "https://github.com/teyfikoz/Travel_Purpose-City_Tags",
        "Bug Tracker": "https://github.com/teyfikoz/Travel_Purpose-City_Tags/issues",
    },
    packages=find_packages(exclude=["tests", "tests.*", "scripts", "examples"]),
    package_data={
        "travelpurpose": [
            "data/*.csv",
            "data/*.parquet",
            "data/*.json",
            "ontology/*.yaml",
        ],
    },
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pyarrow>=12.0.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "requests-cache>=1.1.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pydantic>=2.0.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "tqdm>=4.65.0",
        "sentence-transformers>=2.2.0",
        "scikit-learn>=1.3.0",
        "openpyxl>=3.1.0",
        "SPARQLWrapper>=2.0.0",
        "urllib3>=2.0.0",
        "playwright>=1.40.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
            "black>=23.0.0",
            "jupyterlab>=4.0.0",
            "notebook>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tpurpose=travelpurpose.cli:app",
        ],
    },
    keywords=[
        "travel",
        "city",
        "classification",
        "tourism",
        "purpose",
        "tags",
        "data-engineering"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    zip_safe=False,
)
