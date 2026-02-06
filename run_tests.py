#!/usr/bin/env python
"""
Test runner script for the Django Bitcoin Tracker application.
This script runs both Django's built-in tests and pytest tests.
"""
import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=False)
    return result.returncode == 0


def main():
    """Main test runner function"""
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("Django Bitcoin Tracker - Test Suite Runner")
    print("=" * 60)
    
    # List of tests to run
    tests = [
        ("python -m pipenv run python manage.py check", "Django System Checks"),
        ("python -m pipenv run python manage.py check --deploy", "Django Deployment Checks"),
        ("python -m pipenv run python manage.py test --verbosity=2", "Django Built-in Tests"),
        ("python -m pipenv run pytest -v", "Pytest Unit Tests"),
        ("python -m pipenv run pytest -m integration -v", "Integration Tests"),
        ("python -m pipenv run pytest -m unit -v", "Unit Tests Only"),
        ("python -m pipenv run pytest --cov=. --cov-report=term-missing", "Coverage Tests"),
    ]
    
    # Optional tests (may fail in some environments)
    optional_tests = [
        ("python -m pipenv run pytest -m slow -v", "Performance Tests"),
        ("python -m pipenv run flake8 .", "Code Style Check (flake8)"),
        ("python -m pipenv run black --check .", "Code Formatting Check (black)"),
        ("python -m pipenv run isort --check-only .", "Import Sorting Check (isort)"),
        ("python -m pipenv run pip-audit", "Security Vulnerability Check"),
        ("python -m pipenv run bandit -r . --exclude ./tests,./venv,./env", "Security Linting (bandit)"),
    ]
    
    results = []
    
    # Run main tests
    for command, description in tests:
        success = run_command(command, description)
        results.append((description, success))
    
    # Run optional tests
    print(f"\n{'='*60}")
    print("Running Optional Tests (failures are non-critical)")
    print(f"{'='*60}")
    
    for command, description in optional_tests:
        try:
            success = run_command(command, description)
            results.append((description, success, True))  # True indicates optional
        except Exception as e:
            print(f"Optional test failed: {e}")
            results.append((description, False, True))
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    required_passed = 0
    required_total = 0
    optional_passed = 0
    optional_total = 0
    
    for result in results:
        if len(result) == 2:  # Required test
            description, success = result
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {description}")
            required_total += 1
            if success:
                required_passed += 1
        else:  # Optional test
            description, success, _ = result
            status = "✅ PASS" if success else "⚠️  FAIL (optional)"
            print(f"{status} {description}")
            optional_total += 1
            if success:
                optional_passed += 1
    
    print(f"\nRequired Tests: {required_passed}/{required_total} passed")
    print(f"Optional Tests: {optional_passed}/{optional_total} passed")
    
    # Exit with appropriate code
    if required_passed == required_total:
        print("\n🎉 All required tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {required_total - required_passed} required tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()