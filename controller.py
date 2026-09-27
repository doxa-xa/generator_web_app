import socket
import struct
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def calculate_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0: 
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

def fetch_generator_data():
    now = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S")
    request = struct.pack('>BBHH', int(os.environ['SLAVE_ID']), 3, 0, 100)
    request += calculate_crc(request)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.5) # Малко под 3 секунди, за да не увисва уеб сървърът
        s.connect((os.environ['IP'], int(os.environ['PORT'])))
        s.sendall(request)
        response = s.recv(1024)
        s.close()
        
        if response and len(response) >= 5:
            payload = response[3:-2] 
            count = len(payload) // 2 
            registers = list(struct.unpack('>' + 'H'*count, payload))
            return registers
        else:
            return []
            
    except socket.timeout:
        print("Contoller connection error: Socket Timeout!")
        with open("controller_log.txt","a") as log:
            log.write(f"{now} | Socket Timeout")
            log.write("\n")
        return []
    except Exception as e:
        print(f"An exeption occured: {e}")
        with open("controller_log.txt","a") as log:
            log.write(f"{now} | An Exception occured: {e}")
        return []
