"""
Tests for URL routing in the home app
"""
import pytest
from django.urls import reverse, resolve
from django.test import TestCase
from home import views


class URLTestCase(TestCase):
    """Test URL routing using Django's built-in testing framework"""
    
    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view"""
        url = reverse('index')
        self.assertEqual(url, '/')
        
        resolver = resolve('/')
        self.assertEqual(resolver.func, views.index)
    
    def test_bitcoin_price_api_url_resolves(self):
        """Test that the Bitcoin price API URL resolves correctly"""
        url = reverse('bitcoin_price_api')
        self.assertEqual(url, '/api/bitcoin-price/')
        
        resolver = resolve('/api/bitcoin-price/')
        self.assertEqual(resolver.func, views.bitcoin_price_api)


@pytest.mark.django_db
class TestURLsPytest:
    """Test URL routing using pytest"""
    
    @pytest.mark.unit
    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view"""
        url = reverse('index')
        assert url == '/'
        
        resolver = resolve('/')
        assert resolver.func == views.index
    
    @pytest.mark.unit
    def test_bitcoin_price_api_url_resolves(self):
        """Test that the Bitcoin price API URL resolves correctly"""
        url = reverse('bitcoin_price_api')
        assert url == '/api/bitcoin-price/'
        
        resolver = resolve('/api/bitcoin-price/')
        assert resolver.func == views.bitcoin_price_api
    
    @pytest.mark.unit
    def test_url_names_are_correct(self):
        """Test that URL names are correctly defined"""
        # Test that we can reverse lookup by name
        index_url = reverse('index')
        api_url = reverse('bitcoin_price_api')
        
        assert index_url == '/'
        assert api_url == '/api/bitcoin-price/'