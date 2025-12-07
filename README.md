# Serial Tool

A Python utility for serial port detection and communication testing.

## Features

- **Auto Port Detection**: Automatically scans and identifies bundle serial ports
- **Manual Port Override**: Option to manually specify a port
- **Serial Communication**: Built-in functions for sending commands and waiting for responses

## Files

| File | Description |
|------|-------------|
| `port_finder.py` | Scans available COM ports and identifies bundle devices |
| `init_check.py` | Serial communication utilities and test functions |

## Requirements

```bash
pip install pyserial
```

## Usage

### Auto Port Detection

By default, the tool automatically detects the bundle port:

```python
from init_check import ser, init_test, wait_serial_keywords

# Port is auto-detected
init_test("MyTest")
```

### Manual Port Specification

Edit `init_check.py` to specify a port manually:

```python
# Set your port here
MANUAL_PORT = '/dev/ttyUSB0'  # Linux/macOS
# MANUAL_PORT = 'COM3'        # Windows
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MANUAL_PORT` | `None` | Manual port override (auto-detect if None) |
| `baudrate` | `3000000` | Serial communication baud rate |
| `ssid` | `"YOU_SSID"` | WiFi SSID for testing |
| `pw` | `"YOUR_PSK"` | WiFi password for testing |

## API Reference

### `init_test(value)`
Initialize a test session with the given test name.

### `wait_serial_keywords(test_name, keyword, command, wait_time=1, debug=False, use_regex=True)`
Send a command and wait for a keyword response.

### `wait_serial_read(test_name, keyword, command, wait_time=1, debug=False, use_regex=True)`
Send a command and read bulk data, waiting for a keyword match.

### `gen_random_string(length)`
Generate a random alphanumeric string.

### `gen_random_num(length)`
Generate a random numeric string.

## License

MIT
