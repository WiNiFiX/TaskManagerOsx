# Python Process Monitor

A Python GUI application that displays all running system processes in a grid format using Tkinter and psutil.

## Features

- 800x600 pixel window
- Real-time process monitoring
- Grid display of running processes with:
  - Process ID (PID)
  - Process Name
  - CPU Usage (%)
  - Memory Usage (%)
  - Process Status
  - Username
- Auto-refresh capability (every 5 seconds)
- Manual refresh button
- Sorted by CPU usage (highest first)
- Cross-platform compatibility

## Requirements

- Python 3.6 or higher
- Tkinter (included with Python standard library)
- psutil library for process monitoring

## Installation

1. **Install Python** (if not already installed):
   - Visit [python.org](https://www.python.org/downloads/)
   - Download and install Python for your operating system
   - Make sure to check "Add Python to PATH" during installation

2. **Verify Python installation**:
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Install required dependencies**:
   ```bash
   pip3 install -r requirements.txt
   # or
   pip install -r requirements.txt
   ```

4. **Clone or download this project**:
   ```bash
   git clone <repository-url>
   cd pythontest
   ```

## Running the Application

1. **Run the application**:
   ```bash
   python main.py
   # or
   python3 main.py
   ```

2. **The application will open** with an 800x600 window containing:
   - Process grid showing all running processes
   - Refresh button to manually update the list
   - Auto-refresh checkbox for automatic updates
   - Status bar showing last update time

## Project Structure

```
pythontest/
├── main.py          # Main application file with process monitoring
├── requirements.txt # Project dependencies (psutil)
├── run.py          # Convenient runner script
├── run.bat         # Windows batch file
└── README.md       # This file
```

## Usage

- **Process Grid**: Displays all running processes sorted by CPU usage
- **Refresh Button**: Click to manually update the process list
- **Auto-refresh**: Check the box to automatically refresh every 5 seconds
- **Scroll**: Use scrollbars to navigate through the process list
- **Sorting**: Processes are automatically sorted by CPU usage (highest first)

## Process Information Displayed

- **PID**: Process ID number
- **Name**: Process name (truncated to 30 characters)
- **CPU %**: Current CPU usage percentage
- **Memory %**: Current memory usage percentage
- **Status**: Process status (running, sleeping, etc.)
- **User**: Username running the process

## Customization

You can easily modify the application by editing `main.py`:
- Change refresh interval by modifying the `time.sleep(5)` value
- Add new columns by modifying the `columns` list and `get_processes()` method
- Change sorting criteria in the `load_processes()` method
- Modify window size by changing the `geometry()` call

## Troubleshooting

- **If you get "psutil not found"**: Run `pip3 install psutil`
- **If you get "tkinter not found"**: Install Python with Tkinter support
- **On macOS**: Both Tkinter and psutil should work with standard Python installation
- **On Linux**: Install `python3-tk` and `python3-psutil` packages if needed
- **On Windows**: Both libraries should work with standard Python installation

## Performance Notes

- The application uses threading to avoid blocking the UI during process enumeration
- Process information is cached and updated efficiently
- Auto-refresh can be disabled to reduce system load
- Large numbers of processes may take a moment to load initially

## License

This project is open source and available under the MIT License. 