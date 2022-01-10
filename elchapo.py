import serial
from time import sleep #Kan vara nödvändigt
import time, datetime, csv
import keyboard #Det här är dumt, men det enklaste jag hittade. *nix system måste köra som Root, vilket inte är önskvärt.

usb_serialport = 'COM4'
time_add = 5 #Testa, måste tweakas under riktiga förhållanden för att inte evaluate_data funktionen ska gå sönder.
sleep_time = 0 #Detta borde vara samma värde som arduino delay.
timeout = 0

ser = serial.Serial(usb_serialport) #Öppna serialporten

def read_data(line): #Läser datan som skickas från arduino via serial. Datan konverteras till en lista och returneras.
    li = list(line.split(" "))
    li_float = []
    try:
        for element in li:
            li_float.append(float(element))
    except:
        print("corrupted data")
    return li_float

def evaluate_data(line): #Kontrollerar brytvärde för datainsamling.

    record_data = False

    if line[0] > 2:
        record_data = True

    if line[1] > 2:
        record_data = True

    if line[2] > 11:
        record_data = True
        
    return record_data

def write_output_data(line):

    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
    datestamp = datetime.date.today()
    line.insert(0, timestamp)
    file_name = str(datestamp) + ".csv"

    with open(file_name, 'a') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(line)

while True:
    try:
        line = ser.readline().decode().strip()
    except:
        print("error, cant read lines")
    
    if evaluate_data(read_data(line)) == True:
        timeout = time.time()+time_add

    if time.time() < timeout:
        write_output_data(read_data(line))
        print("DATA RECORDED: ", read_data(line))
        
    else:
        print("DATA OUTPUT: ", read_data(line))
    sleep(sleep_time)

    if keyboard.is_pressed('q'):
        print("End loop")
        break

ser.close()
