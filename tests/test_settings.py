"""
Tests for Django settings configuration
"""
import pytest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SettingsTestCase(TestCase):
    """Test Django settings using built-in testing framework"""
    
    def test_debug_setting(self):
        """Test that DEBUG setting is properly configured"""
        self.assertIsInstance(settings.DEBUG, bool)
    
    def test_secret_key_exists(self):
        """Test that SECRET_KEY is set"""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '')
    
    def test_installed_apps_contains_required_apps(self):
        """Test that required apps are in INSTALLED_APPS"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'home',
        ]
        
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)
    
    def test_database_configuration(self):
        """Test that database is properly configured"""
        self.assertIn('default', settings.DATABASES)
        self.assertIn('ENGINE', settings.DATABASES['default'])
        self.assertIn('NAME', settings.DATABASES['default'])
    
    def test_middleware_configuration(self):
        """Test that required middleware is configured"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        
        for middleware in required_middleware:
            self.assertIn(middleware, settings.MIDDLEWARE)
    
    def test_templates_configuration(self):
        """Test that templates are properly configured"""
        self.assertTrue(len(settings.TEMPLATES) > 0)
        template_config = settings.TEMPLATES[0]
        self.assertEqual(template_config['BACKEND'], 'django.template.backends.django.DjangoTemplates')
        self.assertTrue(template_config['APP_DIRS'])


@pytest.mark.django_db
class TestSettingsPytest:
    """Test Django settings using pytest"""
    
    @pytest.mark.unit
    def test_debug_setting(self):
        """Test that DEBUG setting is properly configured"""
        assert isinstance(settings.DEBUG, bool)
    
    @pytest.mark.unit
    def test_secret_key_exists(self):
        """Test that SECRET_KEY is set"""
        assert hasattr(settings, 'SECRET_KEY')
        assert settings.SECRET_KEY is not None
        assert settings.SECRET_KEY != ''
    
    @pytest.mark.unit
    def test_installed_apps_contains_home_app(self):
        """Test that home app is in INSTALLED_APPS"""
        assert 'home' in settings.INSTALLED_APPS
    
    @pytest.mark.unit
    def test_database_is_sqlite(self):
        """Test that database is configured to use SQLite"""
        assert 'default' in settings.DATABASES
        assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'
    
    @pytest.mark.unit
    def test_time_zone_setting(self):
        """Test that timezone is properly set"""
        assert hasattr(settings, 'TIME_ZONE')
        assert settings.TIME_ZONE == 'UTC'
    
    @pytest.mark.unit
    def test_language_code_setting(self):
        """Test that language code is properly set"""
        assert hasattr(settings, 'LANGUAGE_CODE')
        assert settings.LANGUAGE_CODE == 'en-us'