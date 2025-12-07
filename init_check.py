import re
import time
from pathlib import Path
import logging
import serial
from port_finder import PortFinder
import port_finder

# You can manually specify a port here, e.g.: MANUAL_PORT = '/dev/ttyUSB0' or MANUAL_PORT = 'COM3'
# If set to None or empty string, it will automatically search from port_finder
MANUAL_PORT = None

# Prioritize manually specified port, otherwise auto-detect
if MANUAL_PORT:
    selected_port = MANUAL_PORT
    print(f"Using manually specified port: {selected_port}")
else:
    finder = PortFinder()
    ports = finder.get_port()
    selected_port = ports.get('bundle', 'Not found')
    print(f"Auto-detected port: {selected_port}")

ser = serial.Serial()
ser.baudrate = 3000000
ser.port = selected_port
ssid = "YOU_SSID"
pw = "YOUR_PSK"
wlan_secure = "wpa2"


def init_test(value):
    print("\n\n=======================================")
    print(f"<<< {value} test >>>")
    print("=======================================")
    ser.close()
    time.sleep(0.2)
    ser.open()
    ser.write(b"\r\n")

def wait_serial_keywords(test_name, keyword, command, wait_time=1, debug=False, use_regex=True):
    start_time = time.time()
    ser.timeout = int(wait_time) + 1
    ser.write(bytes(command.encode()))
    received_data = [] 
    while True:
        data = ser.readline()
        elapsed_time = time.time() - start_time
        decoded_data = data.decode('ascii', errors='ignore').strip()
        if debug:
            print(decoded_data)
            logging.info(decoded_data)
        if decoded_data:  # record non-empty data
            received_data.append(decoded_data)
        if use_regex:
            if re.search(keyword, decoded_data):
                print(f"{test_name} PASS")
                logging.info(f"{test_name} PASS")
                for line in received_data:
                    logging.info(line)
                return True, received_data
        else:
            if keyword in decoded_data:
                print(f"{test_name} PASS")
                logging.info(f"{test_name} PASS")
                for line in received_data:
                    logging.info(line)
                return True

        if elapsed_time >= wait_time:
            print(f"{test_name} FAILED")
            logging.error(f"{test_name} FAILED")
            for line in received_data:
                logging.error(line)
            return False


def wait_serial_read(test_name, keyword, command, wait_time=1, debug=False, use_regex=True):
    start_time = time.time()
    ser.timeout = int(wait_time) + 1
    ser.write(bytes(command.encode()))
    received_data = []
    
    while True:
        # 讀取更大的數據塊
        data = ser.read(ser.in_waiting or 32768)  # 讀取更大的緩衝區
        elapsed_time = time.time() - start_time
        
        if data:
            decoded_data = data.decode('ascii', errors='ignore').strip()
            if debug:
                print(decoded_data)
                logging.info(decoded_data)
            if decoded_data:
                received_data.append(decoded_data)
                
            if use_regex:
                if re.search(keyword, decoded_data):
                    print(f"{test_name} PASS")
                    logging.info(f"{test_name} PASS")
                    for line in received_data:
                        logging.info(line)
                    return True, received_data
            else:
                if keyword in decoded_data:
                    print(f"{test_name} PASS")
                    logging.info(f"{test_name} PASS")
                    for line in received_data:
                        logging.info(line)
                    return True
                    
        if elapsed_time >= wait_time:
            print(f"{test_name} FAILED")
            logging.error(f"{test_name} FAILED")
            for line in received_data:
                logging.error(line)
            return False


def gen_random_string(length):
    import random
    import string
    characters = string.digits + string.ascii_lowercase
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def gen_random_num(length):
    import random
    import string
    characters = string.digits
    random_num = ''.join(random.choice(characters) for _ in range(length))
    return random_num