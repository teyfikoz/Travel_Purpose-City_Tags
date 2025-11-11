#!/usr/bin/env python3
"""
Build and release script for TravelPurpose.

Validates package before release.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Error: {description} failed!")
        sys.exit(1)


def main():
    """Main release validation flow."""
    print("TravelPurpose Release Build Script")
    print("=" * 60)

    # Clean previous builds
    run_command("make clean", "Cleaning previous builds")

    # Run linters
    run_command("ruff check travelpurpose/ tests/", "Running Ruff linter")
    run_command("black --check travelpurpose/ tests/", "Checking code formatting")

    # Run tests
    run_command("pytest --cov=travelpurpose --cov-report=term-missing", "Running test suite")

    # Build package
    run_command("python -m build", "Building package")

    # Check package
    run_command("twine check dist/*", "Validating package")

    print("\n" + "=" * 60)
    print("✓ All checks passed! Package is ready for release.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update version in pyproject.toml")
    print("2. Update CHANGELOG.md")
    print("3. Commit changes")
    print("4. Create git tag: git tag v0.1.0")
    print("5. Push tag: git push origin v0.1.0")
    print("6. GitHub Actions will automatically publish to PyPI")
    print("\nOr manually upload:")
    print("  twine upload dist/*")


if __name__ == "__main__":
    main()
