#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from core.ai_handler import AIHandler

def main():
    # Test AI handler initialization
    try:
        handler = AIHandler("test_key")
        print("AI Handler initialized successfully!")
        
        # Test basic functionality
        print("\nTesting state management:")
        print(f"Initial state: {handler.state}")
        
        print("\nTesting cache initialization:")
        print(f"Cache directory exists: {os.path.exists('cache')}")
        
    except Exception as e:
        print(f"Error testing AI Handler: {e}")

if __name__ == "__main__":
    main()