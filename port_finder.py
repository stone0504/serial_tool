import serial
import serial.tools.list_ports
import time
import logging

class PortFinder:
    def __init__(self, baudrate=3000000):
        self.port_list = {}
        self.baudrate = baudrate

    def get_port(self):
        """
        Find bundle COM ports
        """
        ports = serial.tools.list_ports.comports(include_links=False)
        print('Starting to search for bundle ports...')
        
        for port in ports:
            # Stops searching for ports if both red and blue ports are found
            if len(self.port_list) == 1:
                break
                
            try:
                with serial.Serial(port=port.device, baudrate=self.baudrate, timeout=1) as port_test:
                    try_count = 0
                    while try_count <= 3:
                        port_test.write(b'help\r')
                        read_all = port_test.read_all().decode('ascii', errors='ignore').split('\n')
                        
                        for x in read_all:
                            if not x.strip():
                                continue
                            if 'Command' in x.strip():
                                self.port_list['bundle'] = port.device
                                logging.info(f'Bundle port found: {port.device}')
                        time.sleep(0.1)
                        try_count += 1
                        
            except Exception as e:
                print(f"Error opening port {port.device}: {e}")
        
        return self.port_list

def test_port_finder(port_count=2):
    test_count = 1
    while test_count <= 3:
        ports = PortFinder().get_port()
        if len(ports) == 1:
            print("\nPorts found:")
            print(f"Bundle port: {ports.get('bundle', 'Not found')}")
            return True
        else:
            print(f"Failed to find Bundle ports, retry: {test_count}")
            time.sleep(1.5)
            test_count += 1
    print("Failed to find Bundle ports, retrying...")
    return False        


if __name__ == "__main__":
    test_port_finder()