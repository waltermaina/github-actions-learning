"""
Tests for models in the home app
"""
import pytest
from django.test import TestCase
from django.db import models
from home import models as home_models


class ModelsTestCase(TestCase):
    """Test models using Django's built-in testing framework"""
    
    def test_no_models_defined(self):
        """Test that no models are currently defined in the home app"""
        # Get all model classes from the home app
        model_classes = [
            getattr(home_models, name) 
            for name in dir(home_models) 
            if isinstance(getattr(home_models, name), type) 
            and issubclass(getattr(home_models, name), models.Model)
            and getattr(home_models, name) != models.Model
        ]
        
        # Should be empty since no models are defined
        self.assertEqual(len(model_classes), 0)


@pytest.mark.django_db
class TestModelsPytest:
    """Test models using pytest"""
    
    @pytest.mark.unit
    def test_no_models_defined(self):
        """Test that no models are currently defined in the home app"""
        # Get all model classes from the home app
        model_classes = [
            getattr(home_models, name) 
            for name in dir(home_models) 
            if isinstance(getattr(home_models, name), type) 
            and issubclass(getattr(home_models, name), models.Model)
            and getattr(home_models, name) != models.Model
        ]
        
        # Should be empty since no models are defined
        assert len(model_classes) == 0
    
    @pytest.mark.unit
    def test_models_module_exists(self):
        """Test that the models module exists and is importable"""
        assert hasattr(home_models, 'models')
        assert home_models.models is not None