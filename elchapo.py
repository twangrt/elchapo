import serial
from time import sleep 
import time, datetime, csv
import keyboard     #Det här är dumt, men det enklaste jag hittade. *nix system måste köra som Root, vilket inte är önskvärt.

usb_serialport = 'COM3'

time_add = 5        #Testa, måste tweakas under riktiga förhållanden.
sleep_time = 0      #Detta borde vara samma värde som arduino delay.
timeout = 0

#Värden för datainsamling
x_trigger_min = -0.2
x_trigger_max = 0.2
y_trigger_min = -0.2
y_trigger_max = 0.2
z_trigger_min = 10.0
z_trigger_max = 10.7
x_running_list = []
y_running_list = []
z_running_list = []
running_list_N = 10


ser = serial.Serial(usb_serialport,19200) #Öppna serialporten

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
    
    x_running_list.append(line[0])
    y_running_list.append(line[1])
    z_running_list.append(line[2])
    
    if len(x_running_list) > running_list_N:
        del x_running_list[0]
        del y_running_list[0]
        del z_running_list[0]
    
    x_mean_value = sum(x_running_list) / len(x_running_list)
    y_mean_value = sum(y_running_list) / len(y_running_list)
    z_mean_value = sum(z_running_list) / len(z_running_list)
    
    record_data = False

    if not x_trigger_min < x_mean_value < x_trigger_max:
        record_data = True

    if not y_trigger_min < y_mean_value < y_trigger_max:
        record_data = True

    if not z_trigger_min < z_mean_value < z_trigger_max:
        record_data = True
        
    return record_data

def write_output_data(line):

    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
    datestamp = datetime.date.today()
    li_string = []
    for element in line:
        li_string.append(str(element).replace('.',','))
    li_string.insert(0, timestamp)
    file_name = str(datestamp) + ".csv"

    with open(file_name, 'a', newline="") as csvfile:
        data_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(li_string)

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
