import unittest
import sys
import os

# Add src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.system_handler import SystemHandler
from utils.config import Config
from utils.logger import Logger

class TestSystemHandler(unittest.TestCase):
    def setUp(self):
        self.system_handler = SystemHandler()
    
    def test_system_info(self):
        info = self.system_handler.get_system_info()
        self.assertIsInstance(info, dict)
        self.assertIn('os', info)
        self.assertIn('cpu', info)
        self.assertIn('memory_total', info)
    
    def test_resource_usage(self):
        usage = self.system_handler.get_resource_usage()
        self.assertIsInstance(usage, dict)
        self.assertIn('cpu_percent', usage)
        self.assertIn('memory_percent', usage)
        self.assertIn('disk_percent', usage)

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config('test_config.json')
    
    def test_default_config(self):
        self.assertIsInstance(self.config.config, dict)
        self.assertIn('character', self.config.config)
        self.assertIn('ai', self.config.config)
        self.assertIn('voice', self.config.config)
    
    def test_get_set_config(self):
        test_value = "test_value"
        self.config.set('character.test_key', test_value)
        self.assertEqual(self.config.get('character.test_key'), test_value)
    
    def tearDown(self):
        if os.path.exists('test_config.json'):
            os.remove('test_config.json')

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger('test_logger')
    
    def test_logger_creation(self):
        self.assertIsNotNone(self.logger)
        self.logger.info("Test log message")
        # Check if log file was created
        log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
        self.assertTrue(len(log_files) > 0)
    
    def tearDown(self):
        # Clean up log files
        for f in os.listdir('logs'):
            if f.endswith('.log'):
                os.remove(os.path.join('logs', f))
        os.rmdir('logs')

if __name__ == '__main__':
    unittest.main()