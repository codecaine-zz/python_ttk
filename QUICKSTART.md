# Quick Start Guide

## TTK Benchmark Test App - Quick Start

### Installation
1. Ensure Python 3.8+ is installed
2. Install dependencies: `pip install psutil`
3. Run: `python main.py` or `python launch.py`

### Basic Usage
1. **Adjust test parameters** in the input fields
2. **Run individual tests** using the test buttons
3. **Run all tests** with the "Run All Tests" button
4. **View results** in the Results section and Performance Summary

### Key Features
- **Theme Testing**: Compare performance across different TTK themes
- **System Monitoring**: Real-time CPU and memory usage
- **Result Management**: Save/load test results in JSON/CSV formats
- **Stress Testing**: Run intensive tests with configurable parameters
- **HTML Reports**: Generate comprehensive performance reports

### Advanced Features
- **Comparison Mode**: Compare multiple test runs (Tools → Compare Results)
- **Stress Testing**: High-load testing (Tools → Stress Test Mode)
- **Performance Monitor**: Real-time system monitoring (Tools → Performance Monitor)
- **HTML Reports**: Detailed reports with analysis (Tools → Generate Report)

### File Structure
```
python_ttk/
├── main.py              # Main application
├── launch.py            # Simple launcher with error checking
├── test_setup.py        # Dependency verification script
├── config.json          # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md           # Full documentation
├── examples/           # Example scripts
│   ├── simple_demo.py  # Basic treeview demo
│   └── theme_comparison.py # Theme performance comparison
└── (generated files)   # Auto-saved results and reports
```

### Keyboard Shortcuts
- **Cmd/Ctrl+S**: Save results
- **Cmd/Ctrl+O**: Load results
- **Cmd/Ctrl+Q**: Quit application

### Tips
- Run tests multiple times for consistent results
- Close other applications for accurate performance measurements
- Use stress testing to identify performance limits
- Compare results across different themes and settings
- Generate HTML reports for detailed analysis

### Troubleshooting
- **Missing psutil**: Run `pip install psutil`
- **Theme errors**: Try different themes from the dropdown
- **Performance issues**: Reduce test parameters or close other apps
- **UI problems**: Check system resources and Python version

For detailed documentation, see README.md
