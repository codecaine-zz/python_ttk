# TTK Benchmark Test App

A comprehensive benchmarking tool for testing Tkinter/TTK performance across different systems and configurations. This application provides detailed performance metrics for various GUI operations and helps developers optimize their Tkinter applications.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### Core Benchmarking Tests
- **Treeview Population**: Measures performance of adding large numbers of items to TTK Treeview widgets
- **Label/Progressbar Updates**: Tests rapid UI element update performance  
- **Window Creation/Destruction**: Benchmarks window management performance
- **Bulk Widget Creation**: Tests creation of large numbers of TTK widgets
- **Memory Allocation Testing**: Measures memory allocation and deallocation performance

### Enhanced Features
- **Theme Switching**: Real-time TTK theme changing with support for all available themes
- **System Information Display**: Shows detailed system specs including CPU, memory, and platform info
- **Performance Monitoring**: Real-time CPU and memory usage monitoring
- **Results Management**: Save, load, and export test results in JSON and CSV formats
- **Auto-save Functionality**: Automatically save results after test completion
- **Threading Support**: Non-blocking test execution with cancellation support
- **Performance Summary**: Comprehensive analysis of all test results
- **Keyboard Shortcuts**: Quick access to common functions
- **Results Comparison**: Compare multiple test runs to track performance changes
- **Stress Testing**: Run tests with increased loads and multiple iterations
- **HTML Report Generation**: Create detailed HTML reports with charts and analysis
- **Configuration Management**: Customizable default settings and thresholds
- **Verbose Output Mode**: Detailed logging for debugging and analysis

### User Interface
- **Professional Layout**: Clean, organized interface with labeled sections
- **Progress Tracking**: Visual progress indicators during test execution
- **Scrollable Results**: Scrollable areas for large datasets and detailed results
- **Context Menus**: Full menu system with File, Tools, and Help options
- **Responsive Design**: Adaptive layout that works on different screen sizes

## Installation

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually comes with Python)
- psutil (for system monitoring)

### Setup
1. Clone or download the repository:
```bash
git clone <repository-url>
cd python_ttk
```

2. Install required dependencies:
```bash
pip install psutil
```

3. Run the application:
```bash
python main.py
```

## Usage

### Running Individual Tests

1. **Treeview Test**:
   - Set the number of items to populate (default: 1000)
   - Click "Test Treeview Population"
   - Results show items populated and time taken

2. **Label/Progress Test**:
   - Set the number of updates (default: 5000)
   - Click "Test Label/Progress Updates"
   - Watch the progress bar and dynamic label updates

3. **Window Creation Test**:
   - Set the number of windows to create (default: 50)
   - Click "Test Window Creation/Destruction"
   - Observe windows being created and destroyed

4. **Widget Creation Test**:
   - Set the number of widget sets (default: 200)
   - Click "Test Bulk Widget Creation"
   - A new window opens showing created widgets

5. **Memory Test**:
   - Set memory size in MB (default: 100)
   - Click "Test Memory Usage"
   - Results show allocation, write, and cleanup times

### Running All Tests
- Click "Run All Tests" to execute all benchmarks sequentially
- Use "Cancel Tests" to stop execution early
- Results are automatically saved if auto-save is enabled

### Advanced Features

#### Results Comparison
- Tools → Compare Results to compare multiple test runs
- Shows performance differences and improvements
- Tracks performance trends over time

#### Stress Testing
- Tools → Stress Test Mode for intensive testing
- Configurable iterations and load multipliers
- Generates comprehensive performance statistics

#### HTML Reports
- Tools → Generate Report creates detailed HTML reports
- Includes charts, analysis, and recommendations
- Can be opened directly in web browser

### Managing Results
- **Save Results**: File → Save Results (Cmd+S)
- **Load Results**: File → Load Results (Cmd+O)
- **Export to CSV**: File → Export to CSV
- **Reset**: File → Reset All Tests

### Customization
- **Theme Selection**: Change TTK themes from the dropdown menu
- **Auto-save**: Toggle automatic result saving
- **System Info**: Show/hide system information panel

## Test Metrics

### Performance Indicators
- **Items/Updates per second**: Rate of operations
- **Creation/Destruction time**: Window management speed
- **Memory efficiency**: Allocation and cleanup performance
- **UI responsiveness**: How well the interface remains interactive

### System Information
- Operating system and version
- CPU cores and frequency
- Memory usage and availability
- Python and Tkinter versions
- Available TTK themes

## File Formats

### JSON Results Format
```json
{
  "timestamp": "2025-05-25 10:30:45",
  "system_info": {
    "platform": "macOS-14.0-arm64",
    "python_version": "3.11.0",
    "cpu_count": 8,
    "memory_total_gb": 16
  },
  "test_results": {
    "treeview": {
      "items": 1000,
      "duration": 0.1234,
      "rate": 8103.2
    }
  }
}
```

### CSV Export Format
```csv
Test,Metric,Value,Unit
treeview,items,1000,count
treeview,duration,0.1234,seconds
treeview,rate,8103.2,count
```

## Keyboard Shortcuts

- **Cmd+S** (Mac) / **Ctrl+S** (Windows/Linux): Save results
- **Cmd+O** (Mac) / **Ctrl+O** (Windows/Linux): Load results
- **Cmd+Q** (Mac) / **Ctrl+Q** (Windows/Linux): Quit application

## Advanced Features

### Performance Monitor
Access Tools → Performance Monitor to view:
- Real-time CPU usage
- Memory consumption graphs
- System resource utilization

### System Information
View detailed system specs via Tools → System Information:
- Hardware configuration
- Software versions
- Available themes
- Performance capabilities

### Batch Testing
- Run multiple test configurations
- Compare results across different settings
- Export data for external analysis

## Troubleshooting

### Common Issues

1. **"psutil not found" error**:
   ```bash
   pip install psutil
   ```

2. **Theme switching fails**:
   - Some themes may not be available on your system
   - Try different themes from the dropdown

3. **Performance seems slow**:
   - Reduce test parameters for faster execution
   - Close other applications to free system resources
   - Check system info for resource availability

4. **Tests won't run**:
   - Ensure Python 3.8+ is installed
   - Verify Tkinter is available
   - Check console for error messages

### Platform-Specific Notes

- **macOS**: Uses 'aqua' theme by default
- **Windows**: May use 'vista' or 'win32' themes
- **Linux**: Typically uses 'clam' or 'alt' themes

## Performance Optimization Tips

### For Better Test Results
1. Close unnecessary applications
2. Run tests multiple times and average results
3. Use consistent test parameters
4. Monitor system resources during testing

### For Application Development
1. Use the results to identify performance bottlenecks
2. Test on target deployment platforms
3. Compare different widget configurations
4. Optimize based on real-world usage patterns

## Contributing

Contributions are welcome! Areas for improvement:
- Additional benchmark tests
- Better visualization of results
- Cross-platform compatibility enhancements
- Performance optimization suggestions

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## Version History

### Version 2.0 (Current)
- Added theme switching
- System monitoring capabilities
- Result saving/loading
- Performance summary
- Threading support
- Memory testing
- Enhanced UI

### Version 1.0
- Basic benchmark tests
- Simple UI
- Core functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Details

### Dependencies
- **tkinter**: GUI framework (built-in with Python)
- **psutil**: System and process monitoring
- **threading**: Non-blocking test execution
- **json**: Result data persistence
- **csv**: Data export functionality

### Architecture
- Object-oriented design
- Event-driven GUI
- Threaded test execution
- Modular test functions
- Extensible result storage

### Performance Considerations
- Tests designed to minimize interference
- Periodic UI updates for responsiveness
- Memory-efficient data structures
- Optimized widget creation patterns

## Support

For issues, questions, or contributions:
- Check the troubleshooting section
- Review existing issues
- Create a new issue with detailed information
- Include system information and error messages

---

**Happy Benchmarking!** 🚀

Use this tool to optimize your Tkinter applications and ensure they perform well across different systems and configurations.
