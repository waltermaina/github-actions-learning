# Django Application with Pipenv

This is a Django Bitcoin Price Tracker application that displays real-time Bitcoin price data with comprehensive testing coverage.

## Features

- **Real-time Bitcoin Price Display**: Fetches current Bitcoin price from CoinGecko API
- **Responsive Web Interface**: Modern, mobile-friendly design with dark theme
- **Automatic Updates**: Price updates every 5 minutes with countdown timer
- **Comprehensive Data**: Shows price, 24h high/low, market cap, volume, and price change
- **Error Handling**: Graceful handling of API failures and network issues
- **Caching**: API responses cached for 5 minutes to improve performance
- **Security**: CSRF protection, input validation, and secure error handling

## Project Structure

```
github-actions-learning/
├── Pipfile              # Pipenv configuration file
├── Pipfile.lock         # Locked dependencies
├── manage.py            # Django management script
├── myproject/           # Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py      # Django settings (includes 'home' app)
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py
├── home/                # Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py         # Comprehensive test suite
│   ├── test_urls.py     # URL routing tests
│   ├── test_models.py   # Model tests
│   ├── urls.py          # App URL configuration
│   ├── views.py         # Main views with Bitcoin API integration
│   └── templates/
│       └── home/
│           └── index.html  # Bitcoin tracker interface
├── tests/               # Additional test modules
│   ├── test_settings.py    # Django settings tests
│   ├── test_project_urls.py # Project URL tests
│   ├── test_frontend.py    # Frontend and template tests
│   ├── test_performance.py # Performance tests
│   └── test_security.py    # Security tests
├── conftest.py          # Pytest configuration and fixtures
├── pytest.ini          # Pytest settings
├── run_tests.py         # Comprehensive test runner
├── TESTING.md           # Detailed testing documentation
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or 3.12
- pipenv

### Installation

1. Install Django and dependencies using pipenv:
   ```bash
   python -m pipenv install
   ```

2. Install development dependencies (for testing):
   ```bash
   python -m pipenv install --dev
   ```

3. Activate the virtual environment:
   ```bash
   python -m pipenv shell
   ```

4. Run database migrations:
   ```bash
   python -m pipenv run python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python -m pipenv run python manage.py runserver
   ```

### Usage

- Visit http://127.0.0.1:8000/ to see the Bitcoin price tracker
- Visit http://127.0.0.1:8000/admin/ to access the Django admin interface
- API endpoint: http://127.0.0.1:8000/api/bitcoin-price/ (returns JSON data)

### Commands

- Start development server: `python -m pipenv run python manage.py runserver`
- Apply database migrations: `python -m pipenv run python manage.py migrate`
- Create superuser: `python -m pipenv run python manage.py createsuperuser`
- Run all tests: `python run_tests.py`
- Run Django tests: `python -m pipenv run python manage.py test`
- Run pytest: `python -m pipenv run pytest`

## Testing

This application includes comprehensive test coverage with both Django's built-in testing framework and pytest.

### Quick Test Commands

```bash
# Run all tests with comprehensive reporting
python run_tests.py

# Run Django built-in tests
python -m pipenv run python manage.py test --verbosity=2

# Run pytest with coverage
python -m pipenv run pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test categories
python -m pipenv run pytest -m unit -v          # Unit tests only
python -m pipenv run pytest -m integration -v   # Integration tests only
python -m pipenv run pytest -m slow -v          # Performance tests
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Views, URL routing, settings, and utility functions
- **Integration Tests**: Full page rendering and API integration
- **Performance Tests**: Load time and caching performance
- **Security Tests**: CSRF protection, input validation, error handling
- **Frontend Tests**: Template rendering, JavaScript functionality, responsive design

### Code Quality

```bash
# Code style checking
python -m pipenv run flake8 .

# Code formatting
python -m pipenv run black .

# Import sorting
python -m pipenv run isort .

# Security scanning
python -m pipenv run safety check
python -m pipenv run bandit -r .
```

For detailed testing information, see [TESTING.md](TESTING.md).

## API Endpoints

### GET /api/bitcoin-price/

Returns current Bitcoin price data in JSON format:

```json
{
  "price": 45000.50,
  "high_24h": 46000.00,
  "low_24h": 44000.00,
  "market_cap": 850000000000,
  "volume_24h": 25000000000,
  "price_change_percentage_24h": 2.5,
  "last_updated": "2024-01-01T12:00:00.000Z"
}
```

**Features:**
- Cached for 5 minutes to improve performance
- Comprehensive error handling for network issues
- Timeout protection (10 seconds)
- Only accepts GET requests

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that runs:

1. **Testing**: Django tests and pytest with multiple Python versions
2. **Code Quality**: Linting with flake8, formatting with black, import sorting with isort
3. **Security**: Vulnerability scanning with safety and bandit
4. **Coverage**: Code coverage reporting with Codecov integration
5. **Performance**: Integration and performance testing

The workflow runs on Ubuntu environments and supports Python 3.11 and 3.12.

## Security Features

- **CSRF Protection**: Enabled for all forms and state-changing operations
- **Input Validation**: Proper validation and sanitization of all inputs
- **Error Handling**: Secure error messages that don't leak sensitive information
- **Timeout Protection**: External API calls have timeout limits
- **Caching**: Secure caching implementation with appropriate cache headers

## Performance Optimizations

- **API Caching**: Bitcoin price data cached for 5 minutes
- **Efficient Templates**: Optimized template rendering with minimal database queries
- **Static File Handling**: Proper static file configuration for production
- **Responsive Design**: Mobile-optimized interface with efficient CSS

## Development

### Adding New Features

1. Write tests first (TDD approach)
2. Implement the feature
3. Ensure all tests pass
4. Update documentation
5. Run code quality checks

### Code Style

The project follows:
- **PEP 8** style guidelines
- **Black** code formatting
- **isort** import sorting
- **flake8** linting

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving
5. Set up HTTPS
6. Configure caching (Redis recommended)
7. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Implement the feature
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

This application serves as a comprehensive example of:
- Modern Django development practices
- Comprehensive testing strategies
- CI/CD pipeline implementation
- Security best practices
- Performance optimization techniques
- External API integration with proper error handling