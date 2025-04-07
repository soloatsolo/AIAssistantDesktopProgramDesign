import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name: str = "AI_Assistant"):
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create handlers
        log_file = f"logs/{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        # Set levels
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.INFO)
        
        # Create formatters and add them to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def critical(self, message: str):
        self.logger.critical(message)

# Custom exception classes
class AIAssistantError(Exception):
    """Base exception class for AI Assistant"""
    pass

class ConfigurationError(AIAssistantError):
    """Raised when there's a configuration error"""
    pass

class AIError(AIAssistantError):
    """Raised when there's an error with AI processing"""
    pass

class SystemError(AIAssistantError):
    """Raised when there's a system-related error"""
    pass