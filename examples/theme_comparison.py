#!/usr/bin/env python3
"""
Theme Comparison Demo
Shows how different themes affect performance
"""

import tkinter as tk
from tkinter import ttk
import time

class ThemeComparison:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Theme Performance Comparison")
        self.root.geometry("600x500")
        
        self.style = ttk.Style()
        self.results = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Theme selection
        theme_frame = ttk.LabelFrame(main_frame, text="Theme Selection", padding="10")
        theme_frame.pack(fill=tk.X, pady=5)
        
        self.theme_var = tk.StringVar(value=self.style.theme_use())
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                  values=list(self.style.theme_names()), state="readonly")
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        ttk.Button(theme_frame, text="Test Current Theme", 
                  command=self.test_theme_performance).pack(side=tk.LEFT, padx=5)
        ttk.Button(theme_frame, text="Test All Themes", 
                  command=self.test_all_themes).pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Results treeview
        columns = ("Theme", "Widget Creation", "Updates", "Total")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120)
        
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).pack(pady=5)
    
    def change_theme(self, event=None):
        try:
            self.style.theme_use(self.theme_var.get())
            self.status_var.set(f"Changed to theme: {self.theme_var.get()}")
        except tk.TclError as e:
            self.status_var.set(f"Theme error: {e}")
    
    def test_theme_performance(self):
        theme_name = self.theme_var.get()
        self.status_var.set(f"Testing theme: {theme_name}")
        self.root.update()
        
        # Test widget creation
        start_time = time.perf_counter()
        test_window = tk.Toplevel(self.root)
        test_window.title(f"Testing {theme_name}")
        
        # Create various widgets
        for i in range(50):
            frame = ttk.Frame(test_window)
            ttk.Label(frame, text=f"Label {i}").pack(side=tk.LEFT)
            ttk.Button(frame, text="Button").pack(side=tk.LEFT)
            ttk.Entry(frame, width=10).pack(side=tk.LEFT)
            frame.pack(anchor="w")
        
        creation_time = time.perf_counter() - start_time
        
        # Test updates
        start_time = time.perf_counter()
        label = ttk.Label(test_window, text="Update test")
        label.pack()
        
        for i in range(1000):
            label.config(text=f"Update {i}")
            if i % 100 == 0:
                test_window.update_idletasks()
        
        update_time = time.perf_counter() - start_time
        total_time = creation_time + update_time
        
        test_window.destroy()
        
        # Store and display results
        self.results[theme_name] = {
            'creation': creation_time,
            'updates': update_time,
            'total': total_time
        }
        
        # Update results display
        # Remove existing entry for this theme
        for item in self.results_tree.get_children():
            if self.results_tree.item(item)['values'][0] == theme_name:
                self.results_tree.delete(item)
        
        # Add new entry
        self.results_tree.insert('', 'end', values=(
            theme_name,
            f"{creation_time:.3f}s",
            f"{update_time:.3f}s", 
            f"{total_time:.3f}s"
        ))
        
        self.status_var.set(f"Completed test for {theme_name}")
    
    def test_all_themes(self):
        themes = list(self.style.theme_names())
        total_themes = len(themes)
        
        for i, theme in enumerate(themes):
            self.status_var.set(f"Testing {theme} ({i+1}/{total_themes})")
            self.theme_var.set(theme)
            self.change_theme()
            self.root.update()
            time.sleep(0.1)  # Brief pause for theme change
            self.test_theme_performance()
        
        # Find best and worst performers
        if self.results:
            best_theme = min(self.results.items(), key=lambda x: x[1]['total'])
            worst_theme = max(self.results.items(), key=lambda x: x[1]['total'])
            
            self.status_var.set(f"Best: {best_theme[0]} ({best_theme[1]['total']:.3f}s), "
                               f"Worst: {worst_theme[0]} ({worst_theme[1]['total']:.3f}s)")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ThemeComparison()
    app.run()
