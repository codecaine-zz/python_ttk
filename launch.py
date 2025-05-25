#!/usr/bin/env python3
"""
TTK Benchmark App Launcher
Simple launcher script with error handling
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are available."""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter (usually comes with Python)")
    
    try:
        import psutil
    except ImportError:
        missing.append("psutil (install with: pip install psutil)")
    
    if missing:
        print("Missing dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nPlease install missing dependencies and try again.")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("TTK Benchmark Test App")
    print("=" * 30)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("All dependencies found. Starting application...")
    
    try:
        # Import and run the main application
        from main import TTKBenchmarkApp
        import tkinter as tk
        
        root = tk.Tk()
        app = TTKBenchmarkApp(root)
        
        print("Application started successfully!")
        print("Close the GUI window to exit.")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Please check that all files are present and dependencies are installed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
