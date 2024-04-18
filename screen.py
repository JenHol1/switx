#Importing libraries
import serial
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO

print("Imported Libraries") #Debug

GPIO.setmode(GPIO.BCM) #Setting GPIO Pins
GPIO.setup(27, GPIO.IN) #Sets GPIO Pin 22 as an Input
GPIO.setup(22, GPIO.IN) #Sets GPIO Pin 22 as an Input

def destroy(): #Used to clear the LCD
    lcd.clear()
    
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')    


def loop():
    mcp.output(3, 1)     # turn on LCD backlight
    lcd.begin(16, 2)     # set number of LCD lines and columns


    n=4 #Loop for startup for 5 seconds
    for i in range(0, n): 
        lcd.setCursor(0, 0)    
        lcd.message("     SwiTx \n") #Display SwiTx on the first line of the LCD
        lcd.message (get_time_now()) #Display the current time as the second line of the LCD
        sleep(1) 

    destroy() #Clears LCD

#Switching to B needs to send a 1

    while(True):
            
        if GPIO.input(27) == 1 or GPIO.input(22) == 1: #When the GPIO Pin 27 receives a HIGH signal or the button on the breadboard is pressed
            print("Input was high") #Debugging line
            lcd.setCursor(0, 0)  # set cursor position
            lcd.message ("    Receiving \n") #Spaces are used to centre the text, displays the fact the device is receiving a signal
            lcd.message("    Output B") #Displays the active output
            sleep(1)
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #Starts a serial session with the Arduino
            ser.reset_input_buffer()
            ser.write(b'0') #Sends a 0 to the Arduino
            print("Sent Serial Command of 0")
            if ser.in_waiting > 0: #Awaits for a response from the arduino
                line = ser.readline().decode('utf-8').rstrip() #Decodes the message from the Arduino
                print(line) #Prints that message from the arduino

        if GPIO.input(27) == 0 and GPIO.input(22) == 0: #When GPIO Pin 27 and the breadboard button is not pressed
            print("Input was low") #Debug line
            lcd.setCursor(0, 0) #Setting the cursor position
            lcd.message("    Standby    \n") #Displays that the device is awaiting a signal
            lcd.message("    Output A")   #Displays the active output
            sleep(1)
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #Starts a serial session with the Arduino
            ser.reset_input_buffer()
            ser.write(b'1') #Sends the Arduion a 1
            print("Sent Serial Command of 1")
            if ser.in_waiting > 0: #Awaits a response from the Arduino
                line = ser.readline().decode('utf-8').rstrip() #Decodes the Arduino message
                print(line) #Prints the message from the Arduino


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

if __name__ == '__main__': #Initalise the program
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        GPIO.cleanup()