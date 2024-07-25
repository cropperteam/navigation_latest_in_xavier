# LIDAR Scanner Package

This package provides a simple interface to interact with a LIDAR scanner, specifically designed for the YdLidarX4 model.

## Features

- Connect to the LIDAR scanner via a specified COM port
- Perform continuous scans
- Process raw LIDAR data
- Detect objects in specific areas (front, right, back, left)

## Usage

```python
from lidar_package import LidarScanner

# Initialize the scanner
scanner = LidarScanner('COM5')  # Replace 'COM5' with your actual COM port

# Perform a single scan
trigger = scanner.scan()
if trigger:
    print("Trigger array:", trigger)
else:
    print("Scan failed or no objects detected")

# For continuous scanning:
try:
    while True:
        trigger = scanner.scan()
        if trigger:
            print("Trigger array:", trigger)
        else:
            print("Scan failed or no objects detected")
except KeyboardInterrupt:
    print("Scanning stopped by user")
```

## API Reference

### `LidarScanner(port)`

Initialize a LIDAR scanner object.

- `port`: The COM port to which the LIDAR is connected (e.g., 'COM5' or '/dev/ttyUSB0')

### `LidarScanner.scan()`

Perform a single scan and return the trigger array.

Returns:
- A list of 4 elements [front, right, back, left] representing the detected distances in each direction.
- `None` if the scan fails or no objects are detected.

## Dependencies

- pyserial
- math

## Note

Ensure that you have the necessary permissions to access the specified COM port.
```

2. For the main README file (to be placed in the root of your GitHub repository):

```markdown
# LIDAR Scanner Project

This project provides a Python package for interacting with a YdLidarX4 LIDAR scanner. It allows for easy connection, scanning, and object detection using the LIDAR data.

## Package: lidar_package

The `lidar_package` folder contains the main LIDAR scanner package. For detailed information about the package, its usage, and API, please refer to the [package README](./lidar_package/README.md).

### Key Features

- Connect to YdLidarX4 via serial port
- Perform continuous scanning
- Process raw LIDAR data
- Detect objects in specific areas (front, right, back, left)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. Install the required dependencies:
   ```
   pip install pyserial
   ```

## Quick Start

1. Connect your YdLidarX4 to your computer.

2. Update the COM port in `main.py`:
   ```python
   com_port = 'COM5'  # Change this to your actual COM port
   ```

3. Run the main script:
   ```
   python main.py
   ```

This will start continuous scanning and print the trigger array for each scan.

## Project Structure

```
.
├── lidar_package/
│   ├── __init__.py
│   ├── lidar_scanner.py
│   └── README.md
├── main.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
