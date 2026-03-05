import serial
import time

# SERIAL -------------------------------------------------------------------------------------------
port = 'COM4'
baud_rate = 115200

ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

while True:
    string = ser.readline().decode('utf-8').strip()
    print(string)