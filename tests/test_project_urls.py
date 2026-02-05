"""
Tests for main project URL configuration
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib import admin


class ProjectURLTestCase(TestCase):
    """Test main project URLs using Django's built-in testing framework"""
    
    def setUp(self):
        self.client = Client()
    
    def test_admin_url_resolves(self):
        """Test that admin URL resolves correctly"""
        url = reverse('admin:index')
        self.assertTrue(url.startswith('/admin/'))
        
        resolver = resolve('/admin/')
        # Check that it resolves to admin site
        self.assertTrue(hasattr(resolver.func, 'admin_site'))
    
    def test_root_url_includes_home_app(self):
        """Test that root URL includes home app URLs"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_url_requires_authentication(self):
        """Test that admin URL requires authentication"""
        response = self.client.get('/admin/')
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/admin/login/'))


@pytest.mark.django_db
class TestProjectURLsPytest:
    """Test main project URLs using pytest"""
    
    @pytest.mark.unit
    def test_admin_url_resolves(self, client):
        """Test that admin URL resolves correctly"""
        url = reverse('admin:index')
        assert url.startswith('/admin/')
        
        resolver = resolve('/admin/')
        assert hasattr(resolver.func, 'admin_site')
    
    @pytest.mark.unit
    def test_root_url_accessible(self, client):
        """Test that root URL is accessible"""
        response = client.get('/')
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_admin_login_required(self, client):
        """Test that admin requires login"""
        response = client.get('/admin/')
        assert response.status_code == 302
        assert response.url.startswith('/admin/login/')
    
    @pytest.mark.unit
    def test_home_app_urls_included(self, client):
        """Test that home app URLs are properly included"""
        # Test index page
        response = client.get('/')
        assert response.status_code == 200
        
        # Test API endpoint
        response = client.get('/api/bitcoin-price/')
        # Should return 200 or 500 (depending on external API), but not 404
        assert response.status_code != 404