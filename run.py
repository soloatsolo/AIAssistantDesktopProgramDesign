#!/usr/bin/env python3
import os
import sys
import subprocess
import json
from pathlib import Path
import asyncio
import qasync
from PyQt6.QtWidgets import QApplication

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().splitlines()
        
        # Try importing each requirement
        missing = []
        for req in requirements:
            package = req.split('>=')[0]
            try:
                __import__(package.lower())
            except ImportError:
                missing.append(req)
        
        if missing:
            print("Installing missing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("Dependencies installed successfully!")
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        sys.exit(1)

def check_config():
    """Check if config file exists and has required fields"""
    config_path = Path('config.json')
    if not config_path.exists():
        print("Creating initial configuration file...")
        default_config = {
            "character": {
                "gender": "female",
                "style": "anime"
            },
            "ai": {
                "api_key": "",
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7
            },
            "voice": {
                "enabled": True,
                "volume": 1.0,
                "rate": 150
            },
            "window": {
                "position_x": 100,
                "position_y": 100,
                "width": 300,
                "height": 400
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        print("Please edit config.json to add your OpenAI API key before running the application.")
        return False
    return True

def main():
    # Check dependencies
    check_dependencies()
    
    # Check configuration
    if not check_config():
        return
    
    # Add src directory to Python path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    
    # Run the application
    try:
        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)

        from src.main import MainWindow
        window = MainWindow()
        window.show()
        
        # Run the event loop
        with loop:
            loop.run_forever()
            
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()