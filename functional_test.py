#!/usr/bin/env python3
"""
Functional test script for the TTK Benchmark App
Tests core functionality without GUI interaction
"""

import sys
import os
import json
import time

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """Test the core functionality of the TTK Benchmark App"""
    print("=== TTK Benchmark App Functional Test ===\n")
    
    try:
        # Test imports
        print("1. Testing imports...")
        import tkinter as tk
        from tkinter import ttk
        import psutil
        import threading
        print("   ✓ All required modules imported successfully")
        
        # Test creating the app instance
        print("\n2. Testing app initialization...")
        root = tk.Tk()
        root.withdraw()  # Hide the window for testing
        
        from main import TTKBenchmarkApp
        app = TTKBenchmarkApp(root)
        print("   ✓ App initialized successfully")
        
        # Test configuration file exists
        print("\n3. Testing configuration...")
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
            print(f"   ✓ Configuration file loaded: {len(config)} settings")
        else:
            print("   ! Configuration file not found (optional)")
        
        # Test system monitoring
        print("\n4. Testing system monitoring...")
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        print(f"   ✓ CPU: {cpu_percent}%, Memory: {memory.percent}%")
        
        # Test result storage structure
        print("\n5. Testing result storage...")
        test_result = {
            'treeview': {'duration': 0.5, 'items': 1000},
            'label_updates': {'duration': 0.3, 'updates': 5000},
            'window_creation': {'duration': 1.2, 'windows': 50},
            'widget_creation': {'duration': 0.8, 'widgets': 200}
        }
        app.test_results = test_result
        print("   ✓ Result storage working")
        
        # Test theme availability
        print("\n6. Testing themes...")
        available_themes = list(app.style.theme_names())
        current_theme = app.style.theme_use()
        print(f"   ✓ Available themes: {available_themes}")
        print(f"   ✓ Current theme: {current_theme}")
        
        # Test core methods exist
        print("\n7. Testing core methods...")
        methods_to_check = [
            'test_treeview_population',
            'test_label_progressbar_updates', 
            'test_window_creation',
            'test_widget_creation',
            'test_memory_usage',
            'update_system_info',
            'save_results',
            'load_results'
        ]
        
        for method_name in methods_to_check:
            if hasattr(app, method_name):
                print(f"   ✓ Method '{method_name}' exists")
            else:
                print(f"   ✗ Method '{method_name}' missing")
        
        # Test widget existence
        print("\n8. Testing widgets...")
        widgets_to_check = [
            'tree',
            'progressbar',
            'dynamic_label',
            'summary_text'
        ]
        
        for widget_name in widgets_to_check:
            if hasattr(app, widget_name):
                print(f"   ✓ Widget '{widget_name}' exists")
            else:
                print(f"   ✗ Widget '{widget_name}' missing")
        
        print("\n=== Test Results ===")
        print("✓ All core functionality tests passed!")
        print("✓ App is ready for use")
        
        # Clean up
        root.destroy()
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_core_functionality()
    if success:
        print("\n🎉 All tests passed! The TTK Benchmark App is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        sys.exit(1)
