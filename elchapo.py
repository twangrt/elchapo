## SUPERDUPER UNDERSÖKNING 

# Arduino input: Serial.print("9.82 1.04 1.07\n");

import serial
from time import sleep #Kan vara nödvändigt 
import time

ser = serial.Serial('/dev/cu.usbmodem146101')  #Öppna serial port
time_add = 2 #Testa, måste tweakas under riktiga förhållanden för att inte evaluate_data funktionen ska gå sönder.
sleep_time = 0.05 #Detta borde vara samma värde som arduino delay.
timeout = 0


def read_data(line): #Läser datan som skickas från arduino via serial. Datan konverteras till en lista och returneras.
    li = list(line.split(" "))
    li_float = []

    for element in li:
        li_float.append(float(element))

    return li_float

def evaluate_data(line): #Kontrollerar brytvärde för datainsamling.
    
    #timeout = time.time()

    timeout = 0
    
    if line[0] > 1.5:
        timeout = time.time() + time_add

    if line[1] > 1.5:
        timeout = time.time() + time_add

    if line[2] > 1.5:
        timeout = time.time() + time_add
    #print(timeout-time.time()) #Kontrollera intervallet vid användning

    return timeout

def write_output_data(line):

    #SKRIV DATA 
    print("Datta skrivs")
    print(line)


while True:
    line = ser.readline().decode().strip()
    #read_data(line)
    #evaluate_data(read_data(line))

    if time.time() < evaluate_data(read_data(line)):
        write_output_data(read_data(line))

    else:
        print(read_data(line))
        print("ingen data")
    sleep(sleep_time)

ser.close()
