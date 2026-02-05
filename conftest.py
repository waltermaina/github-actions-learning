"""
Global pytest configuration and fixtures
"""
import os
import django
from django.conf import settings

# Configure Django settings before importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    """Django test client fixture"""
    return Client()


@pytest.fixture
def user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Create an admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def mock_bitcoin_api_response():
    """Mock response data for Bitcoin API"""
    return {
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