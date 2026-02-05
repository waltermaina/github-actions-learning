"""
Tests for frontend functionality and template rendering
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from unittest.mock import patch, Mock
import json


class FrontendTestCase(TestCase):
    """Test frontend functionality using Django's built-in testing framework"""
    
    def setUp(self):
        self.client = Client()
        cache.clear()
    
    def test_index_template_contains_required_elements(self):
        """Test that index template contains all required HTML elements"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        # Check for essential HTML elements
        self.assertIn('<title>Bitcoin Price Tracker</title>', content)
        self.assertIn('id="price"', content)
        self.assertIn('id="change"', content)
        self.assertIn('id="high"', content)
        self.assertIn('id="low"', content)
        self.assertIn('id="market-cap"', content)
        self.assertIn('id="volume"', content)
        self.assertIn('id="timestamp"', content)
        self.assertIn('id="countdown"', content)
    
    def test_index_template_contains_javascript_functions(self):
        """Test that index template contains required JavaScript functions"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        # Check for JavaScript functions
        self.assertIn('fetchBitcoinData', content)
        self.assertIn('updateUI', content)
        self.assertIn('formatCurrency', content)
        self.assertIn('startCountdown', content)
        self.assertIn('updateCountdownDisplay', content)
    
    def test_index_template_contains_api_endpoint_reference(self):
        """Test that template references the correct API endpoint"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        self.assertIn('/api/bitcoin-price/', content)
    
    def test_index_template_contains_css_styling(self):
        """Test that template contains CSS styling"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        # Check for CSS variables and styling
        self.assertIn('--bg-color:', content)
        self.assertIn('--card-bg:', content)
        self.assertIn('--text-primary:', content)
        self.assertIn('--accent-color:', content)
        self.assertIn('.container', content)
        self.assertIn('.card', content)
        self.assertIn('.price-display', content)
    
    def test_index_template_responsive_design(self):
        """Test that template includes responsive design elements"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        # Check for responsive meta tag
        self.assertIn('name="viewport"', content)
        self.assertIn('width=device-width', content)
        
        # Check for media queries
        self.assertIn('@media', content)
        self.assertIn('max-width: 600px', content)
    
    def test_index_template_accessibility_features(self):
        """Test that template includes accessibility features"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        # Check for accessibility attributes
        self.assertIn('lang="en"', content)
        # Check for semantic HTML structure
        self.assertIn('<h1>', content)
        self.assertIn('<title>', content)
    
    def test_index_template_contains_error_handling(self):
        """Test that template includes error handling elements"""
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        
        self.assertIn('id="error-message"', content)
        self.assertIn('style="display: none;"', content)


@pytest.mark.django_db
class TestFrontendPytest:
    """Test frontend functionality using pytest"""
    
    def setup_method(self):
        """Setup method called before each test"""
        cache.clear()
    
    @pytest.mark.unit
    def test_index_template_structure(self, client):
        """Test the overall structure of the index template"""
        response = client.get(reverse('index'))
        content = response.content.decode()
        
        # Check HTML5 doctype
        assert '<!DOCTYPE html>' in content
        
        # Check essential HTML structure
        assert '<html lang="en">' in content
        assert '<head>' in content
        assert '<body>' in content
        assert '</html>' in content
    
    @pytest.mark.unit
    def test_javascript_api_integration(self, client):
        """Test that JavaScript properly integrates with API"""
        response = client.get(reverse('index'))
        content = response.content.decode()
        
        # Check that JavaScript makes requests to the correct endpoint
        assert "fetch('/api/bitcoin-price/')" in content
        
        # Check error handling in JavaScript
        assert 'catch (error)' in content
        assert 'console.error' in content
    
    @pytest.mark.unit
    def test_css_variables_defined(self, client):
        """Test that CSS custom properties are properly defined"""
        response = client.get(reverse('index'))
        content = response.content.decode()
        
        css_variables = [
            '--bg-color',
            '--card-bg',
            '--text-primary',
            '--text-secondary',
            '--accent-color',
            '--accent-glow',
            '--danger-color'
        ]
        
        for variable in css_variables:
            assert variable in content
    
    @pytest.mark.unit
    def test_countdown_timer_elements(self, client):
        """Test that countdown timer elements are present"""
        response = client.get(reverse('index'))
        content = response.content.decode()
        
        assert 'id="countdown"' in content
        assert 'countdownSeconds = 300' in content  # 5 minutes
        assert 'setInterval' in content
    
    @pytest.mark.unit
    def test_currency_formatting_function(self, client):
        """Test that currency formatting function is present"""
        response = client.get(reverse('index'))
        content = response.content.decode()
        
        assert 'formatCurrency' in content
        assert 'Intl.NumberFormat' in content
        assert 'currency: \'USD\'' in content
    
    @patch('home.views.requests.get')
    def test_frontend_api_integration_with_mock_data(self, mock_get, client):
        """Test frontend integration with mocked API data"""
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
        
        # Test that the page loads
        response = client.get('/')
        assert response.status_code == 200
        
        # Test that the API endpoint works
        api_response = client.get('/api/bitcoin-price/')
        assert api_response.status_code == 200
        
        data = json.loads(api_response.content)
        assert data['price'] == 45000.50


@pytest.mark.integration
@pytest.mark.django_db
class TestFrontendIntegration:
    """Integration tests for frontend functionality"""
    
    def setup_method(self):
        """Setup method called before each test"""
        cache.clear()
    
    def test_complete_page_rendering(self, client):
        """Test complete page rendering with all components"""
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.content.decode()
        
        # Verify all major sections are present
        sections = [
            'Bitcoin Price Tracker',
            'Real-time Bitcoin price',
            'price-display',
            'details-grid',
            'refresh-indicator'
        ]
        
        for section in sections:
            assert section in content
    
    @patch('home.views.requests.get')
    def test_error_state_handling(self, mock_get, client):
        """Test that error states are properly handled"""
        # Mock API failure
        mock_get.side_effect = Exception("API Error")
        
        # Page should still load
        response = client.get('/')
        assert response.status_code == 200
        
        # API should return error
        api_response = client.get('/api/bitcoin-price/')
        assert api_response.status_code == 500
        
        data = json.loads(api_response.content)
        assert 'error' in data