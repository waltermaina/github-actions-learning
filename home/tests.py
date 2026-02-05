import json
from unittest.mock import patch, Mock
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.core.cache import cache
import requests
from home.views import bitcoin_price_api


class HomeViewsTestCase(TestCase):
    """Test cases for home app views using Django's built-in testing framework"""
    
    def setUp(self):
        self.client = Client()
        # Clear cache before each test to avoid interference
        cache.clear()
    
    def test_index_view_status_code(self):
        """Test that the index view returns a 200 status code"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_uses_correct_template(self):
        """Test that the index view uses the correct template"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'home/index.html')
    
    def test_index_view_contains_expected_content(self):
        """Test that the index view contains expected content"""
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Bitcoin Price Tracker')
        self.assertContains(response, 'Real-time Bitcoin price')
    
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_success(self, mock_get):
        """Test successful Bitcoin API response"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
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
        mock_get.return_value = mock_response
        
        response = self.client.get(reverse('bitcoin_price_api'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['price'], 45000.50)
        self.assertEqual(data['high_24h'], 46000.00)
        self.assertEqual(data['low_24h'], 44000.00)
        self.assertEqual(data['market_cap'], 850000000000)
        self.assertEqual(data['volume_24h'], 25000000000)
        self.assertEqual(data['price_change_percentage_24h'], 2.5)
        self.assertEqual(data['last_updated'], '2024-01-01T12:00:00.000Z')
    
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_external_api_failure(self, mock_get):
        """Test Bitcoin API when external API returns error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        response = self.client.get(reverse('bitcoin_price_api'))
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Failed to fetch data from CoinGecko')
    
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_network_error(self, mock_get):
        """Test Bitcoin API when network error occurs"""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        response = self.client.get(reverse('bitcoin_price_api'))
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Network error occurred')
    
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_timeout_error(self, mock_get):
        """Test Bitcoin API when timeout occurs"""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")
        
        response = self.client.get(reverse('bitcoin_price_api'))
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Network error occurred')
    
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_malformed_response(self, mock_get):
        """Test Bitcoin API with malformed response data"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Empty response
        mock_get.return_value = mock_response
        
        response = self.client.get(reverse('bitcoin_price_api'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Should handle missing data gracefully with defaults
        self.assertEqual(data['price'], 0)
        self.assertEqual(data['high_24h'], 0)
        self.assertEqual(data['low_24h'], 0)
        self.assertEqual(data['market_cap'], 0)
        self.assertEqual(data['volume_24h'], 0)
        self.assertEqual(data['price_change_percentage_24h'], 0)
    
    def test_bitcoin_price_api_only_allows_get(self):
        """Test that Bitcoin API only allows GET requests"""
        # Test POST request
        response = self.client.post(reverse('bitcoin_price_api'))
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        
        # Test PUT request
        response = self.client.put(reverse('bitcoin_price_api'))
        self.assertEqual(response.status_code, 405)
        
        # Test DELETE request
        response = self.client.delete(reverse('bitcoin_price_api'))
        self.assertEqual(response.status_code, 405)
    
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_partial_data(self, mock_get):
        """Test Bitcoin API with partial data in response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'market_data': {
                'current_price': {'usd': 45000.50},
                'high_24h': {'usd': 46000.00},
                # Missing some fields to test defaults
            }
        }
        mock_get.return_value = mock_response
        
        response = self.client.get(reverse('bitcoin_price_api'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['price'], 45000.50)
        self.assertEqual(data['high_24h'], 46000.00)
        self.assertEqual(data['low_24h'], 0)  # Should default to 0
        self.assertEqual(data['market_cap'], 0)
        self.assertEqual(data['volume_24h'], 0)


# Pytest-based tests
@pytest.mark.django_db
class TestHomeViewsPytest:
    """Test cases for home app views using pytest"""
    
    def setup_method(self):
        """Setup method called before each test"""
        cache.clear()
    
    @pytest.mark.unit
    def test_index_view_status_code(self, client):
        """Test that the index view returns a 200 status code"""
        response = client.get(reverse('index'))
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_index_view_uses_correct_template(self, client):
        """Test that the index view uses the correct template"""
        response = client.get(reverse('index'))
        assert 'home/index.html' in [t.name for t in response.templates]
    
    @pytest.mark.unit
    def test_index_view_contains_expected_content(self, client):
        """Test that the index view contains expected content"""
        response = client.get(reverse('index'))
        content = response.content.decode()
        assert 'Bitcoin Price Tracker' in content
        assert 'Real-time Bitcoin price' in content
    
    @pytest.mark.unit
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_success(self, mock_get, client, mock_bitcoin_api_response):
        """Test successful Bitcoin API response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_bitcoin_api_response
        mock_get.return_value = mock_response
        
        response = client.get(reverse('bitcoin_price_api'))
        
        assert response.status_code == 200
        data = json.loads(response.content)
        
        assert data['price'] == 45000.50
        assert data['high_24h'] == 46000.00
        assert data['low_24h'] == 44000.00
        assert data['market_cap'] == 850000000000
        assert data['volume_24h'] == 25000000000
        assert data['price_change_percentage_24h'] == 2.5
    
    @pytest.mark.unit
    @patch('home.views.requests.get')
    def test_bitcoin_price_api_network_error(self, mock_get, client):
        """Test Bitcoin API when network error occurs"""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        response = client.get(reverse('bitcoin_price_api'))
        
        assert response.status_code == 500
        data = json.loads(response.content)
        assert 'error' in data
        assert data['error'] == 'Network error occurred'
    
    @pytest.mark.unit
    def test_bitcoin_price_api_only_allows_get(self, client):
        """Test that Bitcoin API only allows GET requests"""
        response = client.post(reverse('bitcoin_price_api'))
        assert response.status_code == 405
        
        response = client.put(reverse('bitcoin_price_api'))
        assert response.status_code == 405
        
        response = client.delete(reverse('bitcoin_price_api'))
        assert response.status_code == 405


@pytest.mark.integration
@pytest.mark.django_db
class TestIntegration:
    """Integration tests"""
    
    def setup_method(self):
        """Setup method called before each test"""
        cache.clear()
    
    def test_full_page_load_integration(self, client):
        """Test full page load with all components"""
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.content.decode()
        # Check for key elements
        assert 'Bitcoin Price Tracker' in content
        assert '/api/bitcoin-price/' in content  # API endpoint referenced in JS
        assert 'fetchBitcoinData' in content  # JavaScript function
    
    @patch('home.views.requests.get')
    def test_api_endpoint_integration(self, mock_get, client, mock_bitcoin_api_response):
        """Test API endpoint integration"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_bitcoin_api_response
        mock_get.return_value = mock_response
        
        # Test API endpoint
        api_response = client.get('/api/bitcoin-price/')
        assert api_response.status_code == 200
        
        data = json.loads(api_response.content)
        assert 'price' in data
        assert 'high_24h' in data
        assert 'low_24h' in data
        assert 'market_cap' in data
        assert 'volume_24h' in data
        assert 'price_change_percentage_24h' in data


@pytest.mark.unit
class TestUtilityFunctions:
    """Test utility functions and edge cases"""
    
    def setup_method(self):
        """Setup method called before each test"""
        cache.clear()
    
    @pytest.mark.unit
    @patch('home.views.requests.get')
    def test_api_timeout_handling(self, mock_get, client):
        """Test API timeout handling"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        response = client.get(reverse('bitcoin_price_api'))
        assert response.status_code == 500
        
        data = json.loads(response.content)
        assert 'error' in data
        assert data['error'] == 'Network error occurred'
    
    @pytest.mark.unit
    @patch('home.views.requests.get')
    def test_api_connection_error(self, mock_get, client):
        """Test API connection error handling"""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        response = client.get(reverse('bitcoin_price_api'))
        assert response.status_code == 500
        
        data = json.loads(response.content)
        assert 'error' in data
        assert data['error'] == 'Network error occurred'
    
    @pytest.mark.unit
    @patch('home.views.requests.get')
    def test_api_json_decode_error(self, mock_get, client):
        """Test API JSON decode error handling"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        response = client.get(reverse('bitcoin_price_api'))
        assert response.status_code == 500
        
        data = json.loads(response.content)
        assert 'error' in data
        assert data['error'] == 'An unexpected error occurred'
