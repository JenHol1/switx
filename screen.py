#Importing libraries
import serial
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime

import RPi.GPIO as GPIO

print("Imported Libraries")

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.OUT)
print("GPIO Settings created")

def destroy():
    lcd.clear()
    
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')    


def loop():
    mcp.output(3, 1)     # turn on LCD backlight
    lcd.begin(16, 2)     # set number of LCD lines and columns


    n=4
    for i in range(0, n):
        lcd.setCursor(0, 0)    
        lcd.message("     SwiTx \n") #Startup
        lcd.message (get_time_now())
        sleep(1)

    destroy()


    while(True):
            
        if GPIO.input(27) == 1:
            print("Input was high")
            lcd.setCursor(0, 0)  # set cursor position
            lcd.message ("    Receiving \n")
            lcd.message("    Output B")
            sleep(1)
            GPIO.output(22, GPIO.LOW)
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ser.reset_input_buffer()
            ser.write(b'0')
            print("Sent Serial Command of 0")
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)

        if GPIO.input(27) == 0:
            print("Input was low")
            lcd.setCursor(0, 0)
            lcd.message("    Standby    \n")# 
            lcd.message("    Output A")   
            sleep(1)
            GPIO.output(22, GPIO.HIGH)
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ser.reset_input_buffer()
            ser.write(b'1')
            print("Sent Serial Command of 1")
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
            
                
        else:
            print("Something is fucky wucky")


PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()