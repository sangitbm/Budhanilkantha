import os
import importlib
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from unittest.mock import patch

class SettingsTests(TestCase):
    @patch('dotenv.load_dotenv')
    def test_production_secret_key_fails_if_missing(self, mock_load_dotenv):
        """Test that missing SECRET_KEY raises ImproperlyConfigured when DEBUG is False."""
        mock_env = {'DEBUG': 'False'}
        
        with patch.dict(os.environ, mock_env, clear=True):
            with self.assertRaises(ImproperlyConfigured) as context:
                import config.settings as conf_settings
                importlib.reload(conf_settings)
            
            self.assertIn("SECRET_KEY environment variable is required in production.", str(context.exception))

    @patch('dotenv.load_dotenv')
    def test_development_fallback_secret_key(self, mock_load_dotenv):
        """Test that in development (DEBUG=True), a fallback SECRET_KEY is used if missing."""
        mock_env = {'DEBUG': 'True'}
        
        with patch.dict(os.environ, mock_env, clear=True):
            import config.settings as conf_settings
            reloaded_settings = importlib.reload(conf_settings)
            self.assertEqual(reloaded_settings.SECRET_KEY, 'django-insecure-fc9bxo%-lh&me+d_(*n!tz4g3k5g=j0^&5oh*!hsvowitj0qc%')
