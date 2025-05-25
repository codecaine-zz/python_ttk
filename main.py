import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import random
import threading
import json
import csv
import platform
import psutil
import os

class TTKBenchmarkApp:
    def __init__(self, root):
        self.root = root
        root.title("TTK Benchmark Test App")
        root.geometry("800x900") # Adjusted for more content

        # Initialize result storage
        self.test_results = {}
        self.is_running_tests = False
        self.comparison_results = []  # For comparing multiple test runs
        
        # --- Style ---
        self.style = ttk.Style()
        # You can try different themes available on your system
        # e.g., 'aqua' (macOS default), 'clam', 'alt', 'default', 'classic'
        # print(self.style.theme_names()) # To see available themes
        # self.style.theme_use('aqua') # Explicitly set if needed, usually automatic on macOS

        # Create menu bar
        self.create_menu()

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Theme Selection Frame ---
        theme_frame = ttk.LabelFrame(main_frame, text="Theme & Settings", padding="10")
        theme_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=5)
        self.theme_var = tk.StringVar(value=self.style.theme_use())
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=list(self.style.theme_names()), state="readonly", width=15)
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        ttk.Separator(theme_frame, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.auto_save_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(theme_frame, text="Auto-save results", variable=self.auto_save_var).pack(side=tk.LEFT, padx=5)
        
        self.show_system_info_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(theme_frame, text="Show system info", variable=self.show_system_info_var, command=self.toggle_system_info).pack(side=tk.LEFT, padx=5)

        self.verbose_mode_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(theme_frame, text="Verbose output", variable=self.verbose_mode_var).pack(side=tk.LEFT, padx=5)

        # --- System Info Frame ---
        self.system_info_frame = ttk.LabelFrame(main_frame, text="System Information", padding="10")
        self.system_info_frame.pack(fill=tk.X, pady=5)
        self.update_system_info()

        # --- Controls Frame ---
        controls_frame = ttk.LabelFrame(main_frame, text="Benchmark Controls", padding="10")
        controls_frame.pack(fill=tk.X, pady=10)

        # --- Results Frame ---
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # --- Treeview Test ---
        ttk.Label(controls_frame, text="Treeview Items:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tree_items_var = tk.IntVar(value=1000)
        ttk.Entry(controls_frame, textvariable=self.tree_items_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(controls_frame, text="Test Treeview Population", command=self.test_treeview_population).grid(row=0, column=2, padx=5, pady=5)
        self.treeview_result_var = tk.StringVar(value="Treeview: Not run")
        ttk.Label(results_frame, textvariable=self.treeview_result_var).pack(anchor="w")

        # --- Label & Progressbar Update Test ---
        ttk.Label(controls_frame, text="Label Updates:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label_updates_var = tk.IntVar(value=5000)
        ttk.Entry(controls_frame, textvariable=self.label_updates_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(controls_frame, text="Test Label/Progress Updates", command=self.test_label_progressbar_updates).grid(row=1, column=2, padx=5, pady=5)
        self.label_update_result_var = tk.StringVar(value="Label/Progress: Not run")
        ttk.Label(results_frame, textvariable=self.label_update_result_var).pack(anchor="w")
        self.progressbar = ttk.Progressbar(results_frame, orient="horizontal", length=300, mode="determinate")
        self.progressbar.pack(pady=5, anchor="w")
        self.dynamic_label = ttk.Label(results_frame, text="Dynamic Label: Idle")
        self.dynamic_label.pack(anchor="w")


        # --- Window Creation Test ---
        ttk.Label(controls_frame, text="Windows to Create:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.window_count_var = tk.IntVar(value=50)
        ttk.Entry(controls_frame, textvariable=self.window_count_var, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(controls_frame, text="Test Window Creation/Destruction", command=self.test_window_creation).grid(row=2, column=2, padx=5, pady=5)
        self.window_result_var = tk.StringVar(value="Windows: Not run")
        ttk.Label(results_frame, textvariable=self.window_result_var).pack(anchor="w")

        # --- Widget Creation Test ---
        ttk.Label(controls_frame, text="Widgets to Create:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.widget_count_var = tk.IntVar(value=200) # Number of sets of widgets
        ttk.Entry(controls_frame, textvariable=self.widget_count_var, width=10).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(controls_frame, text="Test Bulk Widget Creation", command=self.test_widget_creation).grid(row=3, column=2, padx=5, pady=5)
        self.widget_creation_result_var = tk.StringVar(value="Widget Creation: Not run")
        ttk.Label(results_frame, textvariable=self.widget_creation_result_var).pack(anchor="w")

        # --- Window Creation Test ---
        ttk.Label(controls_frame, text="Memory Test (MB):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.memory_test_var = tk.IntVar(value=100)
        ttk.Entry(controls_frame, textvariable=self.memory_test_var, width=10).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(controls_frame, text="Test Memory Usage", command=self.test_memory_usage).grid(row=4, column=2, padx=5, pady=5)
        self.memory_result_var = tk.StringVar(value="Memory: Not run")
        ttk.Label(results_frame, textvariable=self.memory_result_var).pack(anchor="w")

        # --- Treeview Widget for Testing ---
        treeview_frame = ttk.LabelFrame(results_frame, text="Test Treeview", padding="10")
        treeview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview with columns
        self.tree = ttk.Treeview(treeview_frame, columns=("col1", "col2"), show="headings", height=8)
        self.tree.heading("col1", text="Item")
        self.tree.heading("col2", text="Value")
        self.tree.column("col1", width=150)
        self.tree.column("col2", width=150)
        
        # Add scrollbars for treeview
        tree_v_scroll = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.tree.yview)
        tree_h_scroll = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_v_scroll.set, xscrollcommand=tree_h_scroll.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_v_scroll.grid(row=0, column=1, sticky="ns")
        tree_h_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        treeview_frame.grid_rowconfigure(0, weight=1)
        treeview_frame.grid_columnconfigure(0, weight=1)

        # --- Performance Summary ---
        summary_frame = ttk.LabelFrame(results_frame, text="Performance Summary", padding="10")
        summary_frame.pack(fill=tk.X, pady=10)
        
        self.summary_text = tk.Text(summary_frame, height=6, wrap=tk.WORD)
        summary_scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=summary_scrollbar.set)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Run All Button ---
        run_all_frame = ttk.Frame(controls_frame)
        run_all_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
        
        self.run_all_btn = ttk.Button(run_all_frame, text="Run All Tests", command=self.run_all_tests_threaded)
        self.run_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(run_all_frame, text="Cancel Tests", command=self.cancel_tests, state="disabled")
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_results_btn = ttk.Button(run_all_frame, text="Save Results", command=self.save_results)
        self.save_results_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_results_btn = ttk.Button(run_all_frame, text="Load Results", command=self.load_results)
        self.load_results_btn.pack(side=tk.LEFT, padx=5)

        # --- Miscellaneous Widgets for Visual Check ---
        misc_frame = ttk.LabelFrame(main_frame, text="Sample TTK Widgets", padding="10")
        misc_frame.pack(fill=tk.X, pady=10)

        ttk.Button(misc_frame, text="TTK Button").pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(misc_frame, text="TTK Checkbutton").pack(side=tk.LEFT, padx=5)
        self.radio_var = tk.StringVar(value="opt1")
        ttk.Radiobutton(misc_frame, text="Opt 1", variable=self.radio_var, value="opt1").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(misc_frame, text="Opt 2", variable=self.radio_var, value="opt2").pack(side=tk.LEFT, padx=5)
        self.combobox = ttk.Combobox(misc_frame, values=["Choice 1", "Choice 2", "Choice 3"])
        self.combobox.pack(side=tk.LEFT, padx=5)
        self.combobox.current(0)
        ttk.Scale(misc_frame, from_=0, to=100, orient=tk.HORIZONTAL).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def clear_treeview(self):
        """Clears all items from the treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Results...", command=self.save_results, accelerator="Cmd+S")
        file_menu.add_command(label="Load Results...", command=self.load_results, accelerator="Cmd+O")
        file_menu.add_command(label="Export to CSV...", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Reset All Tests", command=self.reset_all_tests)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Cmd+Q")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="System Information", command=self.show_system_info_window)
        tools_menu.add_command(label="Performance Monitor", command=self.show_performance_monitor)
        tools_menu.add_command(label="Compare Results", command=self.show_comparison_window)
        tools_menu.add_command(label="Stress Test Mode", command=self.show_stress_test_window)
        tools_menu.add_command(label="Clear Treeview", command=self.clear_treeview)
        tools_menu.add_separator()
        tools_menu.add_command(label="Generate Report", command=self.generate_html_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        
        # Keyboard bindings
        self.root.bind('<Command-s>', lambda e: self.save_results())
        self.root.bind('<Command-o>', lambda e: self.load_results())
        self.root.bind('<Command-q>', lambda e: self.root.quit())

    def change_theme(self, event=None):
        """Change the TTK theme."""
        try:
            self.style.theme_use(self.theme_var.get())
        except tk.TclError as e:
            messagebox.showerror("Theme Error", f"Could not apply theme: {e}")

    def update_system_info(self):
        """Update system information display."""
        if not self.show_system_info_var.get():
            return
            
        try:
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            python_version = platform.python_version()
            tk_version = self.root.tk.call('info', 'patchlevel')
            
            info_text = f"OS: {platform.system()} {platform.release()} | "
            info_text += f"CPU: {cpu_count} cores | "
            info_text += f"RAM: {memory.total // (1024**3)}GB ({memory.percent}% used) | "
            info_text += f"Python: {python_version} | Tk: {tk_version}"
            
            if hasattr(self, 'system_info_label'):
                self.system_info_label.destroy()
            self.system_info_label = ttk.Label(self.system_info_frame, text=info_text, font=('TkDefaultFont', 9))
            self.system_info_label.pack(anchor="w")
        except Exception as e:
            print(f"Error updating system info: {e}")

        # Schedule the next update
        if self.show_system_info_var.get():
            self.root.after(5000, self.update_system_info) # Update every 5 seconds

    def toggle_system_info(self):
        """Toggle system info visibility."""
        if self.show_system_info_var.get():
            self.system_info_frame.pack(fill=tk.X, pady=5, before=self.root.children['!frame'].children['!labelframe2'])
            self.update_system_info()
        else:
            self.system_info_frame.pack_forget()

    def test_treeview_population(self):
        """Tests how long it takes to populate the treeview."""
        if self.is_running_tests and hasattr(self, 'test_thread'):
            return
            
        self.clear_treeview()
        num_items = self.tree_items_var.get()
        if num_items <= 0:
            self.treeview_result_var.set("Treeview: Invalid number of items.")
            return

        self.treeview_result_var.set(f"Treeview: Running for {num_items} items...")
        self.root.update_idletasks() # Ensure UI is updated before starting

        start_time = time.perf_counter()
        for i in range(num_items):
            if hasattr(self, 'is_running_tests') and not self.is_running_tests:
                break
            self.tree.insert("", "end", values=(f"Item {i+1}", f"Data {random.randint(0, 1000)}"))
            if i % 100 == 0: # Allow UI to refresh periodically for very large numbers
                self.root.update_idletasks()
        
        # Ensure all items are rendered before stopping timer
        self.root.update_idletasks()
        end_time = time.perf_counter()
        
        duration = end_time - start_time
        self.treeview_result_var.set(f"Treeview: Populated {num_items} items in {duration:.4f} seconds.")
        
        # Store results
        self.test_results['treeview'] = {
            'items': num_items,
            'duration': duration,
            'rate': num_items / duration if duration > 0 else 0
        }

    def test_label_progressbar_updates(self):
        """Tests how long it takes to update a label and progressbar rapidly."""
        num_updates = self.label_updates_var.get()
        if num_updates <= 0:
            self.label_update_result_var.set("Label/Progress: Invalid number of updates.")
            return

        self.label_update_result_var.set(f"Label/Progress: Running {num_updates} updates...")
        self.progressbar["maximum"] = num_updates
        self.root.update_idletasks()

        start_time = time.perf_counter()
        for i in range(num_updates):
            if hasattr(self, 'is_running_tests') and not self.is_running_tests:
                break
            self.dynamic_label.config(text=f"Dynamic Label: Update {i+1}/{num_updates}")
            self.progressbar["value"] = i + 1
            if i % 100 == 0: # Update UI periodically to see changes
                self.root.update_idletasks()
        
        self.dynamic_label.config(text=f"Dynamic Label: Update {num_updates}/{num_updates}")
        self.progressbar["value"] = num_updates
        self.root.update_idletasks() # Ensure final update is rendered
        end_time = time.perf_counter()

        duration = end_time - start_time
        self.label_update_result_var.set(f"Label/Progress: {num_updates} updates in {duration:.4f} seconds.")
        
        # Store results
        self.test_results['label_updates'] = {
            'updates': num_updates,
            'duration': duration,
            'rate': num_updates / duration if duration > 0 else 0
        }

    def test_window_creation(self):
        """Tests creation and destruction of multiple Toplevel windows."""
        num_windows = self.window_count_var.get()
        if num_windows <= 0:
            self.window_result_var.set("Windows: Invalid number of windows.")
            return

        self.window_result_var.set(f"Windows: Creating {num_windows} windows...")
        self.root.update_idletasks()
        
        windows_list = []
        start_time = time.perf_counter()

        for i in range(num_windows):
            win = tk.Toplevel(self.root)
            win.geometry("150x50+{}+{}".format(random.randint(50,800), random.randint(50,600)))
            win.title(f"Test Win {i+1}")
            ttk.Label(win, text=f"Window {i+1}").pack(padx=10, pady=10)
            windows_list.append(win)
            if i % 10 == 0: # Allow UI to refresh
                self.root.update_idletasks()
        
        self.root.update_idletasks() # Ensure all windows are mapped
        creation_time = time.perf_counter()
        creation_duration = creation_time - start_time
        self.window_result_var.set(f"Windows: Created {num_windows} in {creation_duration:.4f}s. Destroying...")
        self.root.update_idletasks()

        # Destruction part
        destroy_start_time = time.perf_counter()
        for win in windows_list:
            win.destroy()
            # self.root.update_idletasks() # Can slow down destruction significantly if uncommented
        
        self.root.update_idletasks() # Ensure all windows are destroyed
        destroy_end_time = time.perf_counter()
        destroy_duration = destroy_end_time - destroy_start_time
        
        total_duration = creation_duration + destroy_duration
        self.window_result_var.set(f"Windows: {num_windows} created in {creation_duration:.4f}s, destroyed in {destroy_duration:.4f}s. Total: {total_duration:.4f}s")
        
        # Store results
        self.test_results['windows'] = {
            'count': num_windows,
            'creation_duration': creation_duration,
            'destroy_duration': destroy_duration,
            'total_duration': total_duration
        }

    def test_widget_creation(self):
        """Tests creation of many miscellaneous ttk widgets in a new window."""
        num_widget_sets = self.widget_count_var.get()
        if num_widget_sets <= 0:
            self.widget_creation_result_var.set("Widget Creation: Invalid number.")
            return

        self.widget_creation_result_var.set(f"Widget Creation: Creating {num_widget_sets} sets...")
        self.root.update_idletasks()

        test_win = tk.Toplevel(self.root)
        test_win.title("Bulk Widget Creation Test")
        test_win.geometry("400x300")
        
        # Create a canvas and a frame inside it to make it scrollable
        canvas = tk.Canvas(test_win)
        scrollbar = ttk.Scrollbar(test_win, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        widgets = []

        start_time = time.perf_counter()
        for i in range(num_widget_sets):
            frame = ttk.Frame(scrollable_frame, padding=2) # Use a frame for each set
            l = ttk.Label(frame, text=f"Set {i+1}:")
            l.pack(side=tk.LEFT)
            widgets.append(l)
            
            b = ttk.Button(frame, text="B")
            b.pack(side=tk.LEFT, padx=1)
            widgets.append(b)
            
            e = ttk.Entry(frame, width=5)
            e.insert(0, str(i))
            e.pack(side=tk.LEFT, padx=1)
            widgets.append(e)

            cb = ttk.Checkbutton(frame, text="C")
            cb.pack(side=tk.LEFT, padx=1)
            widgets.append(cb)
            frame.pack(anchor="w") # Pack the frame itself

            if i % 50 == 0: # Update UI periodically
                self.root.update_idletasks()
        
        self.root.update_idletasks() # Ensure all widgets are mapped
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        self.widget_creation_result_var.set(f"Widget Creation: {num_widget_sets*4} widgets in {num_widget_sets} sets created in {duration:.4f}s.")
        
        # Store results
        self.test_results['widgets'] = {
            'sets': num_widget_sets,
            'widgets': num_widget_sets * 4,
            'duration': duration,
            'rate': (num_widget_sets * 4) / duration if duration > 0 else 0
        }
        
        # Clean up the test window after a delay or on button press
        # For simplicity, we'll leave it open. User can close it.
        # Or add a button to close it:
        # ttk.Button(test_win, text="Close Widget Window", command=test_win.destroy).pack(pady=10)

    def test_memory_usage(self):
        """Test memory allocation and deallocation performance."""
        memory_mb = self.memory_test_var.get()
        if memory_mb <= 0:
            self.memory_result_var.set("Memory: Invalid size.")
            return

        self.memory_result_var.set(f"Memory: Testing {memory_mb}MB allocation...")
        self.root.update_idletasks()

        try:
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            start_time = time.perf_counter()
            
            # Allocate memory
            data = bytearray(memory_mb * 1024 * 1024)
            alloc_time = time.perf_counter()
            
            # Write to memory to ensure it's actually allocated
            for i in range(0, len(data), 1024):
                data[i] = i % 256
            write_time = time.perf_counter()
            
            peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Clean up
            del data
            cleanup_time = time.perf_counter()
            final_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            alloc_duration = alloc_time - start_time
            write_duration = write_time - alloc_time
            cleanup_duration = cleanup_time - write_time
            memory_increase = peak_memory - start_memory
            
            result = f"Memory: {memory_mb}MB - Alloc: {alloc_duration:.4f}s, Write: {write_duration:.4f}s, "
            result += f"Cleanup: {cleanup_duration:.4f}s, Peak: +{memory_increase:.1f}MB"
            self.memory_result_var.set(result)
            
            self.test_results['memory'] = {
                'size_mb': memory_mb,
                'alloc_time': alloc_duration,
                'write_time': write_duration,
                'cleanup_time': cleanup_duration,
                'memory_increase_mb': memory_increase
            }
            
        except Exception as e:
            self.memory_result_var.set(f"Memory: Error - {str(e)}")

    def run_all_tests(self):
        """Runs all benchmark tests sequentially."""
        self.test_treeview_population()
        if not self.is_running_tests:
            return
        self.root.update() # Allow UI to process events & update display
        
        self.test_label_progressbar_updates()
        if not self.is_running_tests:
            return
        self.root.update()
        
        self.test_window_creation()
        if not self.is_running_tests:
            return
        self.root.update()
        
        self.test_widget_creation()
        if not self.is_running_tests:
            return
        self.root.update()
        
        self.test_memory_usage()
        self.root.update()
        self.test_memory_usage()
        self.root.update()
        messagebox.showinfo("Benchmark Tests", "All tests completed.")

    def run_all_tests_threaded(self):
        """Run all tests in a separate thread to prevent UI blocking."""
        if self.is_running_tests:
            return
            
        self.is_running_tests = True
        self.run_all_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        
        def run_tests():
            try:
                self.run_all_tests()
                self.update_performance_summary()
                if self.auto_save_var.get():
                    self.auto_save_results()
            finally:
                self.root.after(0, self.tests_completed)
                
        self.test_thread = threading.Thread(target=run_tests, daemon=True)
        self.test_thread.start()

    def cancel_tests(self):
        """Cancel running tests."""
        self.is_running_tests = False
        self.tests_completed()

    def tests_completed(self):
        """Called when tests are completed or cancelled."""
        self.is_running_tests = False
        self.run_all_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def update_performance_summary(self):
        """Update the performance summary text widget."""
        self.summary_text.delete(1.0, tk.END)
        
        if not self.test_results:
            self.summary_text.insert(tk.END, "No test results available. Run some tests first.")
            return
            
        summary = "PERFORMANCE SUMMARY\n"
        summary += "=" * 50 + "\n\n"
        
        total_time = 0
        for test_name, result in self.test_results.items():
            if test_name == 'treeview' and 'duration' in result:
                summary += f"Treeview Population: {result['items']} items in {result['duration']:.4f}s\n"
                summary += f"  Rate: {result['items']/result['duration']:.0f} items/second\n\n"
                total_time += result['duration']
                
            elif test_name == 'label_updates' and 'duration' in result:
                summary += f"Label/Progress Updates: {result['updates']} in {result['duration']:.4f}s\n"
                summary += f"  Rate: {result['updates']/result['duration']:.0f} updates/second\n\n"
                total_time += result['duration']
                
            elif test_name == 'windows' and 'total_duration' in result:
                summary += f"Window Management: {result['count']} windows\n"
                summary += f"  Creation: {result['creation_duration']:.4f}s\n"
                summary += f"  Destruction: {result['destroy_duration']:.4f}s\n"
                summary += f"  Total: {result['total_duration']:.4f}s\n\n"
                total_time += result['total_duration']
                
            elif test_name == 'widgets' and 'duration' in result:
                summary += f"Widget Creation: {result['widgets']} widgets in {result['duration']:.4f}s\n"
                summary += f"  Rate: {result['widgets']/result['duration']:.0f} widgets/second\n\n"
                total_time += result['duration']
                
            elif test_name == 'memory' and 'alloc_time' in result:
                summary += f"Memory Test: {result['size_mb']}MB\n"
                summary += f"  Allocation: {result['alloc_time']:.4f}s\n"
                summary += f"  Write: {result['write_time']:.4f}s\n"
                summary += f"  Cleanup: {result['cleanup_time']:.4f}s\n\n"
        
        if total_time > 0:
            summary += f"Total Test Time: {total_time:.4f} seconds\n"
            
        summary += f"\nTest completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        self.summary_text.insert(tk.END, summary)

    def save_results(self):
        """Save test results to a JSON file."""
        if not self.test_results:
            messagebox.showwarning("No Results", "No test results to save. Run some tests first.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Test Results"
        )
        
        if filename:
            try:
                save_data = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'system_info': {
                        'platform': platform.platform(),
                        'python_version': platform.python_version(),
                        'cpu_count': psutil.cpu_count(),
                        'memory_total_gb': psutil.virtual_memory().total // (1024**3)
                    },
                    'test_results': self.test_results
                }
                
                with open(filename, 'w') as f:
                    json.dump(save_data, f, indent=2)
                messagebox.showinfo("Saved", f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save results: {e}")

    def load_results(self):
        """Load test results from a JSON file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Test Results"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                self.test_results = data.get('test_results', {})
                self.update_performance_summary()
                
                # Update result labels
                self.update_result_displays()
                
                messagebox.showinfo("Loaded", f"Results loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load results: {e}")

    def export_to_csv(self):
        """Export test results to CSV format."""
        if not self.test_results:
            messagebox.showwarning("No Results", "No test results to export. Run some tests first.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Test Results to CSV"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Test', 'Metric', 'Value', 'Unit'])
                    
                    for test_name, result in self.test_results.items():
                        for key, value in result.items():
                            unit = self.get_unit_for_metric(key)
                            writer.writerow([test_name, key, value, unit])
                
                messagebox.showinfo("Exported", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not export results: {e}")

    def get_unit_for_metric(self, metric):
        """Get the appropriate unit for a metric."""
        if 'time' in metric or 'duration' in metric:
            return 'seconds'
        elif 'count' in metric or 'items' in metric or 'updates' in metric or 'widgets' in metric:
            return 'count'
        elif 'mb' in metric.lower():
            return 'MB'
        else:
            return ''

    def auto_save_results(self):
        """Automatically save results with timestamp."""
        if not self.test_results:
            return
            
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"ttk_benchmark_results_{timestamp}.json"
        
        try:
            save_data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'system_info': {
                    'platform': platform.platform(),
                    'python_version': platform.python_version(),
                    'cpu_count': psutil.cpu_count(),
                    'memory_total_gb': psutil.virtual_memory().total // (1024**3)
                },
                'test_results': self.test_results
            }
            
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Auto-save failed: {e}")

    def reset_all_tests(self):
        """Reset all test results and displays."""
        self.test_results = {}
        self.treeview_result_var.set("Treeview: Not run")
        self.label_update_result_var.set("Label/Progress: Not run")
        self.window_result_var.set("Windows: Not run")
        self.widget_creation_result_var.set("Widget Creation: Not run")
        self.memory_result_var.set("Memory: Not run")
        self.clear_treeview()
        self.summary_text.delete(1.0, tk.END)
        self.dynamic_label.config(text="Dynamic Label: Idle")
        self.progressbar["value"] = 0

    def update_result_displays(self):
        """Update result display labels from loaded data."""
        if 'treeview' in self.test_results:
            result = self.test_results['treeview']
            self.treeview_result_var.set(f"Treeview: Populated {result.get('items', 0)} items in {result.get('duration', 0):.4f} seconds.")
            
        if 'label_updates' in self.test_results:
            result = self.test_results['label_updates']
            self.label_update_result_var.set(f"Label/Progress: {result.get('updates', 0)} updates in {result.get('duration', 0):.4f} seconds.")
            
        if 'windows' in self.test_results:
            result = self.test_results['windows']
            self.window_result_var.set(f"Windows: {result.get('count', 0)} created in {result.get('creation_duration', 0):.4f}s, destroyed in {result.get('destroy_duration', 0):.4f}s. Total: {result.get('total_duration', 0):.4f}s")
            
        if 'widgets' in self.test_results:
            result = self.test_results['widgets']
            self.widget_creation_result_var.set(f"Widget Creation: {result.get('widgets', 0)} widgets in {result.get('sets', 0)} sets created in {result.get('duration', 0):.4f}s.")
            
        if 'memory' in self.test_results:
            result = self.test_results['memory']
            self.memory_result_var.set(f"Memory: {result.get('size_mb', 0)}MB - Alloc: {result.get('alloc_time', 0):.4f}s, Write: {result.get('write_time', 0):.4f}s, Cleanup: {result.get('cleanup_time', 0):.4f}s")

    def show_system_info_window(self):
        """Show detailed system information in a new window."""
        info_window = tk.Toplevel(self.root)
        info_window.title("System Information")
        info_window.geometry("500x400")
        
        text_widget = tk.Text(info_window, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(info_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Gather system information
        info = f"SYSTEM INFORMATION\n{'='*50}\n\n"
        info += f"Platform: {platform.platform()}\n"
        info += f"System: {platform.system()} {platform.release()}\n"
        info += f"Architecture: {platform.architecture()[0]}\n"
        info += f"Processor: {platform.processor()}\n"
        info += f"Python Version: {platform.python_version()}\n"
        info += f"Tkinter Version: {self.root.tk.call('info', 'patchlevel')}\n\n"
        
        info += f"CPU Information:\n"
        info += f"  Physical cores: {psutil.cpu_count(logical=False)}\n"
        info += f"  Total cores: {psutil.cpu_count(logical=True)}\n"
        info += f"  Current frequency: {psutil.cpu_freq().current:.2f} MHz\n\n"
        
        memory = psutil.virtual_memory()
        info += f"Memory Information:\n"
        info += f"  Total: {memory.total / (1024**3):.2f} GB\n"
        info += f"  Available: {memory.available / (1024**3):.2f} GB\n"
        info += f"  Used: {memory.used / (1024**3):.2f} GB ({memory.percent}%)\n\n"
        
        info += f"Available TTK Themes:\n"
        for theme in self.style.theme_names():
            current = " (current)" if theme == self.style.theme_use() else ""
            info += f"  {theme}{current}\n"
        
        text_widget.insert(tk.END, info)
        text_widget.config(state="disabled")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_performance_monitor(self):
        """Show a real-time performance monitor window."""
        monitor_window = tk.Toplevel(self.root)
        monitor_window.title("Performance Monitor")
        monitor_window.geometry("400x300")
        
        # CPU and Memory monitoring labels
        cpu_var = tk.StringVar()
        memory_var = tk.StringVar()
        
        ttk.Label(monitor_window, text="Real-time System Monitor", font=('TkDefaultFont', 12, 'bold')).pack(pady=10)
        ttk.Label(monitor_window, textvariable=cpu_var).pack(pady=5)
        ttk.Label(monitor_window, textvariable=memory_var).pack(pady=5)
        
        # Progress bars for visual representation
        cpu_progress = ttk.Progressbar(monitor_window, length=300, mode='determinate')
        cpu_progress.pack(pady=5)
        
        memory_progress = ttk.Progressbar(monitor_window, length=300, mode='determinate')
        memory_progress.pack(pady=5)
        
        def update_monitor():
            if monitor_window.winfo_exists():
                try:
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    memory = psutil.virtual_memory()
                    
                    cpu_var.set(f"CPU Usage: {cpu_percent:.1f}%")
                    memory_var.set(f"Memory Usage: {memory.percent:.1f}% ({memory.used / (1024**3):.1f} GB / {memory.total / (1024**3):.1f} GB)")
                    
                    cpu_progress['value'] = cpu_percent
                    memory_progress['value'] = memory.percent
                    
                    monitor_window.after(1000, update_monitor)
                except:
                    pass
        
        update_monitor()

    def show_about(self):
        """Show about dialog."""
        about_text = """TTK Benchmark Test App
        
A comprehensive benchmarking tool for testing Tkinter/TTK performance.

Features:
• Treeview population testing
• Label and progressbar update performance
• Window creation/destruction timing
• Bulk widget creation testing
• Memory allocation testing
• Theme switching
• Results saving/loading
• Performance monitoring

Version: 2.0
Author: TTK Benchmark Team"""
        
        messagebox.showinfo("About TTK Benchmark", about_text)

    def show_shortcuts(self):
        """Show keyboard shortcuts dialog."""
        shortcuts_text = """Keyboard Shortcuts:

Cmd+S - Save results
Cmd+O - Load results  
Cmd+Q - Quit application

Menu Functions:
File → Save/Load/Export results
Tools → System info, Performance monitor
Help → About, Shortcuts"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)

    def show_comparison_window(self):
        """Show results comparison window."""
        if len(self.comparison_results) < 2:
            if self.test_results:
                # Add current results to comparison if available
                self.comparison_results.append({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'results': self.test_results.copy()
                })
            
            if len(self.comparison_results) < 2:
                messagebox.showinfo("Comparison", "Need at least 2 test results to compare. Run more tests or load additional results.")
                return

        comp_window = tk.Toplevel(self.root)
        comp_window.title("Results Comparison")
        comp_window.geometry("700x500")
        
        # Create notebook for different comparisons
        notebook = ttk.Notebook(comp_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Summary comparison
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary")
        
        # Create comparison table
        columns = ('Test', 'Run 1', 'Run 2', 'Difference', 'Improvement')
        comp_tree = ttk.Treeview(summary_frame, columns=columns, show='headings')
        
        for col in columns:
            comp_tree.heading(col, text=col)
            comp_tree.column(col, width=120)
        
        # Populate comparison data
        if len(self.comparison_results) >= 2:
            run1 = self.comparison_results[-2]['results']
            run2 = self.comparison_results[-1]['results']
            
            for test_name in set(run1.keys()) & set(run2.keys()):
                if 'duration' in run1[test_name] and 'duration' in run2[test_name]:
                    time1 = run1[test_name]['duration']
                    time2 = run2[test_name]['duration']
                    diff = time2 - time1
                    improvement = ((time1 - time2) / time1 * 100) if time1 > 0 else 0
                    
                    comp_tree.insert('', 'end', values=(
                        test_name.title(),
                        f"{time1:.4f}s",
                        f"{time2:.4f}s", 
                        f"{diff:+.4f}s",
                        f"{improvement:+.1f}%"
                    ))
        
        comp_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=comp_tree.yview)
        comp_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(comp_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Add Current Results", 
                  command=lambda: self.add_to_comparison()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Comparison", 
                  command=lambda: self.clear_comparison()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Comparison", 
                  command=lambda: self.export_comparison()).pack(side=tk.LEFT, padx=5)

    def add_to_comparison(self):
        """Add current results to comparison list."""
        if self.test_results:
            self.comparison_results.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'results': self.test_results.copy()
            })
            messagebox.showinfo("Added", f"Results added to comparison. Total runs: {len(self.comparison_results)}")

    def clear_comparison(self):
        """Clear comparison results."""
        self.comparison_results = []
        messagebox.showinfo("Cleared", "Comparison results cleared.")

    def export_comparison(self):
        """Export comparison results to CSV."""
        if len(self.comparison_results) < 2:
            messagebox.showwarning("No Data", "Need at least 2 results to export comparison.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Comparison Results"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Test', 'Metric', 'Run 1', 'Run 2', 'Difference', 'Improvement %'])
                    
                    if len(self.comparison_results) >= 2:
                        run1 = self.comparison_results[-2]['results']
                        run2 = self.comparison_results[-1]['results']
                        
                        for test_name in set(run1.keys()) & set(run2.keys()):
                            for metric in set(run1[test_name].keys()) & set(run2[test_name].keys()):
                                val1 = run1[test_name][metric]
                                val2 = run2[test_name][metric]
                                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                                    diff = val2 - val1
                                    improvement = ((val1 - val2) / val1 * 100) if val1 != 0 else 0
                                    writer.writerow([test_name, metric, val1, val2, diff, f"{improvement:.1f}"])
                
                messagebox.showinfo("Exported", f"Comparison exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not export comparison: {e}")

    def show_stress_test_window(self):
        """Show stress test configuration window."""
        stress_window = tk.Toplevel(self.root)
        stress_window.title("Stress Test Mode")
        stress_window.geometry("400x300")
        
        ttk.Label(stress_window, text="Stress Test Configuration", font=('TkDefaultFont', 12, 'bold')).pack(pady=10)
        
        # Test iterations
        iter_frame = ttk.Frame(stress_window)
        iter_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(iter_frame, text="Test Iterations:").pack(side=tk.LEFT)
        self.stress_iterations_var = tk.IntVar(value=5)
        ttk.Entry(iter_frame, textvariable=self.stress_iterations_var, width=10).pack(side=tk.RIGHT)
        
        # Multiplier
        mult_frame = ttk.Frame(stress_window)
        mult_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(mult_frame, text="Load Multiplier:").pack(side=tk.LEFT)
        self.stress_multiplier_var = tk.DoubleVar(value=2.0)
        ttk.Entry(mult_frame, textvariable=self.stress_multiplier_var, width=10).pack(side=tk.RIGHT)
        
        # Progress
        self.stress_progress = ttk.Progressbar(stress_window, length=300, mode='determinate')
        self.stress_progress.pack(pady=20)
        
        self.stress_status_var = tk.StringVar(value="Ready to start stress test")
        ttk.Label(stress_window, textvariable=self.stress_status_var).pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(stress_window)
        button_frame.pack(pady=20)
        
        self.stress_start_btn = ttk.Button(button_frame, text="Start Stress Test", 
                                          command=self.run_stress_test)
        self.stress_start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stress_stop_btn = ttk.Button(button_frame, text="Stop Test", 
                                         command=self.stop_stress_test, state="disabled")
        self.stress_stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.stress_running = False

    def run_stress_test(self):
        """Run stress test with multiple iterations."""
        iterations = self.stress_iterations_var.get()
        multiplier = self.stress_multiplier_var.get()
        
        if iterations <= 0 or multiplier <= 0:
            messagebox.showerror("Invalid Input", "Iterations and multiplier must be positive numbers.")
            return
        
        self.stress_running = True
        self.stress_start_btn.config(state="disabled")
        self.stress_stop_btn.config(state="normal")
        self.stress_progress["maximum"] = iterations
        
        def stress_test_thread():
            try:
                stress_results = []
                original_values = {}
                
                # Save original test values
                original_values['tree_items'] = self.tree_items_var.get()
                original_values['label_updates'] = self.label_updates_var.get()
                original_values['window_count'] = self.window_count_var.get()
                original_values['widget_count'] = self.widget_count_var.get()
                original_values['memory_test'] = self.memory_test_var.get()
                
                for i in range(iterations):
                    if not self.stress_running:
                        break
                        
                    self.root.after(0, lambda i=i: self.stress_status_var.set(f"Running iteration {i+1}/{iterations}"))
                    self.root.after(0, lambda i=i: setattr(self.stress_progress, 'value', i))
                    
                    # Increase test loads
                    self.tree_items_var.set(int(original_values['tree_items'] * multiplier))
                    self.label_updates_var.set(int(original_values['label_updates'] * multiplier))
                    self.window_count_var.set(int(original_values['window_count'] * multiplier))
                    self.widget_count_var.set(int(original_values['widget_count'] * multiplier))
                    self.memory_test_var.set(int(original_values['memory_test'] * multiplier))
                    
                    # Run tests
                    self.run_all_tests()
                    
                    # Store results
                    if self.test_results:
                        stress_results.append({
                            'iteration': i + 1,
                            'results': self.test_results.copy()
                        })
                    
                    time.sleep(0.5)  # Brief pause between iterations
                
                # Restore original values
                self.tree_items_var.set(original_values['tree_items'])
                self.label_updates_var.set(original_values['label_updates'])
                self.window_count_var.set(original_values['window_count'])
                self.widget_count_var.set(original_values['widget_count'])
                self.memory_test_var.set(original_values['memory_test'])
                
                # Calculate averages and show results
                self.root.after(0, lambda: self.show_stress_results(stress_results))
                
            finally:
                self.root.after(0, self.stress_test_completed)
        
        threading.Thread(target=stress_test_thread, daemon=True).start()

    def stop_stress_test(self):
        """Stop the running stress test."""
        self.stress_running = False

    def stress_test_completed(self):
        """Called when stress test is completed."""
        self.stress_running = False
        self.stress_start_btn.config(state="normal")
        self.stress_stop_btn.config(state="disabled")
        self.stress_status_var.set("Stress test completed")
        self.stress_progress["value"] = self.stress_progress["maximum"]

    def show_stress_results(self, stress_results):
        """Show stress test results summary."""
        if not stress_results:
            messagebox.showinfo("No Results", "No stress test results to display.")
            return
        
        results_window = tk.Toplevel(self.root)
        results_window.title("Stress Test Results")
        results_window.geometry("600x400")
        
        # Create text widget for results
        text_widget = tk.Text(results_window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Calculate averages
        averages = {}
        for result in stress_results:
            for test_name, test_data in result['results'].items():
                if test_name not in averages:
                    averages[test_name] = {}
                for metric, value in test_data.items():
                    if isinstance(value, (int, float)):
                        if metric not in averages[test_name]:
                            averages[test_name][metric] = []
                        averages[test_name][metric].append(value)
        
        # Generate report
        report = "STRESS TEST RESULTS\n"
        report += "=" * 50 + "\n\n"
        report += f"Iterations: {len(stress_results)}\n"
        report += f"Load Multiplier: {self.stress_multiplier_var.get()}\n\n"
        
        for test_name, metrics in averages.items():
            report += f"{test_name.upper()} TEST:\n"
            for metric, values in metrics.items():
                avg = sum(values) / len(values)
                min_val = min(values)
                max_val = max(values)
                report += f"  {metric}: avg={avg:.4f}, min={min_val:.4f}, max={max_val:.4f}\n"
            report += "\n"
        
        text_widget.insert(tk.END, report)
        text_widget.config(state="disabled")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def generate_html_report(self):
        """Generate an HTML report of test results."""
        if not self.test_results:
            messagebox.showwarning("No Results", "No test results to generate report. Run some tests first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Save HTML Report"
        )
        
        if filename:
            try:
                html_content = self.create_html_report()
                with open(filename, 'w') as f:
                    f.write(html_content)
                messagebox.showinfo("Report Generated", f"HTML report saved to {filename}")
                
                # Ask if user wants to open the report
                if messagebox.askyesno("Open Report", "Would you like to open the report in your browser?"):
                    import webbrowser
                    webbrowser.open(f"file://{os.path.abspath(filename)}")
                    
            except Exception as e:
                messagebox.showerror("Report Error", f"Could not generate report: {e}")

    def create_html_report(self):
        """Create HTML content for the test report."""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>TTK Benchmark Report - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        .test-result {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #007acc; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .metric {{ font-weight: bold; }}
        .footer {{ margin-top: 40px; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TTK Benchmark Test Report</h1>
        <p>Generated on: {timestamp}</p>
        <p>Platform: {platform.platform()}</p>
        <p>Python Version: {platform.python_version()}</p>
    </div>
    
    <div class="section">
        <h2>System Information</h2>
        <table>
            <tr><th>Property</th><th>Value</th></tr>
            <tr><td>Operating System</td><td>{platform.system()} {platform.release()}</td></tr>
            <tr><td>CPU Cores</td><td>{psutil.cpu_count()}</td></tr>
            <tr><td>Memory (Total)</td><td>{psutil.virtual_memory().total // (1024**3)} GB</td></tr>
            <tr><td>TTK Theme</td><td>{self.style.theme_use()}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Test Results</h2>"""
        
        for test_name, results in self.test_results.items():
            html += f"""
        <div class="test-result">
            <h3>{test_name.title()} Test</h3>
            <table>
                <tr><th>Metric</th><th>Value</th><th>Unit</th></tr>"""
            
            for metric, value in results.items():
                unit = self.get_unit_for_metric(metric)
                if isinstance(value, float):
                    value_str = f"{value:.4f}"
                else:
                    value_str = str(value)
                html += f"<tr><td class='metric'>{metric}</td><td>{value_str}</td><td>{unit}</td></tr>"
            
            html += "</table></div>"
        
        html += """
    </div>
    
    <div class="section">
        <h2>Performance Summary</h2>
        <div class="test-result">"""
        
        # Add performance analysis
        total_time = sum(result.get('duration', 0) for result in self.test_results.values())
        html += f"<p><strong>Total Test Time:</strong> {total_time:.4f} seconds</p>"
        
        # Add recommendations
        html += """
            <h4>Performance Analysis:</h4>
            <ul>"""
        
        for test_name, result in self.test_results.items():
            if 'rate' in result:
                rate = result['rate']
                if test_name == 'treeview' and rate < 1000:
                    html += "<li>Treeview population rate is below 1000 items/second - consider optimization</li>"
                elif test_name == 'widgets' and rate < 100:
                    html += "<li>Widget creation rate is below 100 widgets/second - UI may feel sluggish</li>"
        
        html += """
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by TTK Benchmark Test App</p>
    </div>
</body>
</html>"""
        
        return html
