# receive_windows
from datetime import datetime
import serial

ser = serial.Serial('COM3',9600)

while(1):
    dt_now = datetime.now()
    distance = ser.readline().decode('utf-8').strip()
    if float(distance) > float(21.0):
        print(f"{dt_now} 在庫なし {distance}")
    elif float(distance) > float(10.0):
        print(f"{dt_now} 在庫あり {distance}")
    else:
        print(f"{dt_now} 在庫大量 {distance}")