#!/usr/bin/env python3
"""
Simple TTK Performance Demo
Demonstrates basic TTK widget performance testing
"""

import tkinter as tk
from tkinter import ttk
import time
import random

def demo_treeview_performance():
    """Demo treeview population performance."""
    root = tk.Tk()
    root.title("Treeview Performance Demo")
    root.geometry("500x400")
    
    # Create treeview
    tree = ttk.Treeview(root, columns=("col1", "col2"), show="headings")
    tree.heading("col1", text="Item")
    tree.heading("col2", text="Value")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Status label
    status_var = tk.StringVar(value="Ready to populate treeview")
    status_label = ttk.Label(root, textvariable=status_var)
    status_label.pack(pady=5)
    
    def populate_tree():
        items = 1000
        status_var.set(f"Populating {items} items...")
        root.update()
        
        start_time = time.perf_counter()
        
        for i in range(items):
            tree.insert("", "end", values=(f"Item {i+1}", random.randint(1, 1000)))
            if i % 100 == 0:
                root.update_idletasks()
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        rate = items / duration
        
        status_var.set(f"Populated {items} items in {duration:.3f}s ({rate:.0f} items/sec)")
    
    def clear_tree():
        for item in tree.get_children():
            tree.delete(item)
        status_var.set("Treeview cleared")
    
    # Buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    
    ttk.Button(button_frame, text="Populate Tree", command=populate_tree).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Clear Tree", command=clear_tree).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Exit", command=root.destroy).pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    demo_treeview_performance()
