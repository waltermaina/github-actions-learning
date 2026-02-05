# Testing Guide for Django Bitcoin Tracker

This document provides comprehensive information about the testing setup and how to run tests for the Django Bitcoin Tracker application.

## Test Structure

The application includes comprehensive test coverage using both Django's built-in testing framework and pytest:

### Test Files Organization

```
├── conftest.py                 # Global pytest configuration and fixtures
├── pytest.ini                 # Pytest configuration
├── home/
│   ├── tests.py               # Main test file with both Django and pytest tests
│   ├── test_urls.py           # URL routing tests
│   └── test_models.py         # Model tests (currently minimal)
├── tests/
│   ├── test_settings.py       # Django settings tests
│   ├── test_project_urls.py   # Main project URL tests
│   ├── test_frontend.py       # Frontend and template tests
│   ├── test_performance.py    # Performance and load tests
│   └── test_security.py       # Security tests
└── run_tests.py               # Comprehensive test runner script
```

## Test Categories

### 1. Unit Tests
- **Django Tests**: Using Django's `TestCase` class
- **Pytest Tests**: Using pytest with Django integration
- **Coverage**: Views, URL routing, settings, and utility functions

### 2. Integration Tests
- Full page rendering tests
- API endpoint integration
- Frontend-backend integration

### 3. Performance Tests
- Page load time tests
- API response time tests
- Caching performance tests
- Concurrent request handling

### 4. Security Tests
- CSRF protection verification
- Input validation tests
- Error handling security
- External API security

### 5. Frontend Tests
- Template rendering tests
- JavaScript functionality tests
- CSS and responsive design tests
- Accessibility tests

## Running Tests

### Prerequisites

1. **Install Dependencies**:
   ```bash
   python -m pipenv install --dev
   ```

2. **Activate Virtual Environment**:
   ```bash
   python -m pipenv shell
   ```

### Quick Test Commands

#### Run All Tests (Recommended)
```bash
python run_tests.py
```

#### Django Built-in Tests Only
```bash
python -m pipenv run python manage.py test --verbosity=2
```

#### Pytest Tests Only
```bash
python -m pipenv run pytest -v
```

#### With Coverage Report
```bash
python -m pipenv run pytest --cov=. --cov-report=html --cov-report=term-missing
```

### Specific Test Categories

#### Unit Tests Only
```bash
python -m pipenv run pytest -m unit -v
```

#### Integration Tests Only
```bash
python -m pipenv run pytest -m integration -v
```

#### Performance Tests (Slow)
```bash
python -m pipenv run pytest -m slow -v
```

#### Security Tests
```bash
python -m pipenv run pytest tests/test_security.py -v
```

#### Frontend Tests
```bash
python -m pipenv run pytest tests/test_frontend.py -v
```

### Individual Test Files

```bash
# Home app tests
python -m pipenv run pytest home/tests.py -v

# URL tests
python -m pipenv run pytest home/test_urls.py -v

# Settings tests
python -m pipenv run pytest tests/test_settings.py -v

# Performance tests
python -m pipenv run pytest tests/test_performance.py -v
```

## Code Quality Checks

### Linting and Formatting

#### Check Code Style (flake8)
```bash
python -m pipenv run flake8 .
```

#### Check Code Formatting (black)
```bash
python -m pipenv run black --check .
```

#### Format Code (black)
```bash
python -m pipenv run black .
```

#### Check Import Sorting (isort)
```bash
python -m pipenv run isort --check-only .
```

#### Fix Import Sorting (isort)
```bash
python -m pipenv run isort .
```

### Security Checks

#### Check for Known Vulnerabilities (safety)
```bash
python -m pipenv run safety check
```

#### Security Linting (bandit)
```bash
python -m pipenv run bandit -r .
```

## Django-Specific Tests

### System Checks
```bash
python -m pipenv run python manage.py check
```

### Deployment Checks
```bash
python -m pipenv run python manage.py check --deploy
```

### Migration Checks
```bash
python -m pipenv run python manage.py makemigrations --check --dry-run
```

### Static Files Check
```bash
python -m pipenv run python manage.py collectstatic --noinput --dry-run
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- Django settings module configuration
- Test discovery patterns
- Custom markers for test categorization
- Verbose output and strict marker enforcement

### Coverage Configuration (`.coveragerc`)
- Source code inclusion/exclusion rules
- Report formatting options
- HTML and XML output configuration

### Code Style Configuration (`setup.cfg`, `pyproject.toml`)
- Flake8 linting rules
- Black formatting options
- Isort import sorting configuration
- Bandit security scanning settings

## Test Fixtures and Mocking

### Available Fixtures (in `conftest.py`)
- `client`: Django test client
- `user`: Test user instance
- `admin_user`: Admin user instance
- `mock_bitcoin_api_response`: Mock Bitcoin API response data

### Mocking External APIs
Tests use `unittest.mock.patch` to mock external API calls:
```python
@patch('home.views.requests.get')
def test_bitcoin_price_api_success(self, mock_get):
    # Mock setup and test implementation
```

## Continuous Integration

The GitHub Actions workflow (`.github/workflows/github-actions-demo.yml`) runs:

1. **Test Job**: Django tests, pytest with coverage
2. **Lint Job**: Code style and formatting checks
3. **Integration Test Job**: Integration and performance tests
4. **Security Scan Job**: Vulnerability and security checks

### Workflow Features
- Multi-Python version testing (3.11, 3.12)
- Ubuntu environment testing
- Coverage reporting with Codecov integration
- Artifact uploading for coverage reports
- Security scanning with safety and bandit

## Test Data and Mocking

### Mock Data Examples
```python
# Bitcoin API response mock
mock_bitcoin_api_response = {
    'market_data': {
        'current_price': {'usd': 45000.50},
        'high_24h': {'usd': 46000.00},
        'low_24h': {'usd': 44000.00},
        'market_cap': {'usd': 850000000000},
        'total_volume': {'usd': 25000000000},
        'price_change_percentage_24h': 2.5,
        'last_updated': '2024-01-01T12:00:00.000Z'
    }
}
```

## Coverage Goals

- **Minimum Coverage**: 80%
- **Target Coverage**: 90%+
- **Critical Components**: 100% (views, API endpoints)

### Viewing Coverage Reports

After running tests with coverage:
```bash
# Terminal report
python -m pipenv run pytest --cov=. --cov-report=term-missing

# HTML report (opens in browser)
python -m pipenv run pytest --cov=. --cov-report=html
# Then open htmlcov/index.html

# XML report (for CI/CD)
python -m pipenv run pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Database Issues**: Tests use in-memory SQLite database
3. **External API Failures**: Tests mock external APIs, shouldn't fail due to network
4. **Permission Issues**: Ensure proper file permissions

### Debug Mode
Run tests with more verbose output:
```bash
python -m pipenv run pytest -vvv --tb=long
```

### Test Database
Tests automatically create and destroy test databases. No manual setup required.

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Dependencies**: Don't rely on external services
3. **Descriptive Test Names**: Use clear, descriptive test method names
4. **Test Both Success and Failure Cases**: Cover happy path and error conditions
5. **Performance Considerations**: Mark slow tests appropriately
6. **Security Testing**: Include security-focused test cases

## Contributing

When adding new features:
1. Write tests for new functionality
2. Ensure existing tests still pass
3. Maintain or improve coverage percentage
4. Follow existing test patterns and naming conventions
5. Update this documentation if needed

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Django Documentation](https://pytest-django.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)