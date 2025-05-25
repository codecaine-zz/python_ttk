#!/usr/bin/env python3
"""
Test script for TTK Benchmark App
Run this to verify all features work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    print("✓ Tkinter imported successfully")
except ImportError:
    print("✗ Tkinter not available")
    sys.exit(1)

try:
    from tkinter import ttk
    print("✓ TTK imported successfully")
except ImportError:
    print("✗ TTK not available")
    sys.exit(1)

try:
    import psutil
    print("✓ psutil imported successfully")
    print(f"  CPU cores: {psutil.cpu_count()}")
    print(f"  Memory: {psutil.virtual_memory().total // (1024**3)}GB")
except ImportError:
    print("✗ psutil not available - install with: pip install psutil")

try:
    import threading
    print("✓ threading module available")
except ImportError:
    print("✗ threading not available")

try:
    import json
    print("✓ json module available")
except ImportError:
    print("✗ json not available")

try:
    import time
    import random
    import platform
    print("✓ Standard library modules available")
    print(f"  Platform: {platform.system()} {platform.release()}")
    print(f"  Python: {platform.python_version()}")
except ImportError:
    print("✗ Some standard library modules missing")

print("\n" + "="*50)
print("Running basic TTK test...")

try:
    root = tk.Tk()
    root.title("TTK Test")
    root.geometry("300x200")
    
    style = ttk.Style()
    print(f"✓ TTK themes available: {list(style.theme_names())}")
    print(f"✓ Current theme: {style.theme_use()}")
    
    # Test basic widgets
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text="TTK Test Window").pack(pady=5)
    ttk.Button(frame, text="Test Button").pack(pady=5)
    ttk.Progressbar(frame, length=200, mode='determinate').pack(pady=5)
    
    # Test treeview
    tree = ttk.Treeview(frame, columns=("col1",), show="headings", height=3)
    tree.heading("col1", text="Test Column")
    tree.insert("", "end", values=("Test Item",))
    tree.pack(pady=5)
    
    print("✓ Basic TTK widgets created successfully")
    
    # Close after a short delay
    root.after(2000, root.destroy)
    root.mainloop()
    
    print("✓ TTK test window completed successfully")
    
except Exception as e:
    print(f"✗ TTK test failed: {e}")

print("\n" + "="*50)
print("All checks completed!")
print("You can now run: python main.py")
