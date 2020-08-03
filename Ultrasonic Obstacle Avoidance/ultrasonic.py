import serial
ser=serial.Serial("/dev/ttyUSB0",9600) #change "USB0" where necessary, if Arduino connected to different serial port
ser.baudrate=9600

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
##important! the '../' portion depends on where the code is stored!
##For more info on this line of code>> https://stackoverflow.com/questions/21005822/what-does-os-path-abspathos-path-joinos-path-dirname-file-os-path-pardir

#import RPi.GPIO as GPIO ##for stuff connected to RPi. use pinMode for arduino instead
import asyncio
import serial_asyncio
from sphero_sdk_rpi_python.sphero_sdk import SpheroRvrAsync
from sphero_sdk_rpi_python.sphero_sdk import SerialAsyncDal
import time
import keyboard
loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    await rvr.wake()
    await rvr.reset_yaw()
    #print (ser.readline()) #for debugging and checking readline
    if ser.readline() == b'Right\r\n':
        print('turning right')
        #await rvr.raw_motors(1,150,2,150) #if you prefer to use this instead of heading
        await rvr.drive_with_heading(0,20,0)
        await asyncio.sleep(0.3) #changed .05 to .1
        await rvr.reset_yaw()
    elif ser.readline() == b'Left\r\n':
        print('turning left')
        #await rvr.raw_motors(2,150,1,150)
        await rvr.drive_with_heading(0,340,0)
        await asyncio.sleep(0.3)
        await rvr.reset_yaw()
    elif ser.readline() == b'Forward\r\n':
        print('forward!')
        await rvr.drive_with_heading(35,0,0)
        await asyncio.sleep(0.2)
        #print(ser.readline())    
##use this if Arduino code includes condition to Reverse
#    elif ser.readline() == b'Obstacle\r\n':
#        await rvr.drive_with_heading(35,180,0)
#        await asyncio.sleep(0.2)
#        print('reversing')

while True:
##in case you want to start/stop the program via keyboard, the code below may be one possible way
    #if state == "sleep" and keyboard.is_pressed('space'):
    #    state = "drive"
    #    time.sleep(0.1) #to prevent multiple triggers in one press
    #elif state == "drive" and keyboard.is_pressed('space'):
    #    state = "sleep"
    #    time.sleep(0.1)
    try:
        loop.run_until_complete(
            asyncio.gather(
                main()
            )
        )
    except KeyboardInterrupt:
        print("Program ended by KeyboardInterrupt")
#         loop.run_until_complete(
#             rvr.close()
#         )
# 
#     finally:
#         if loop.is_running():
#             loop.close()
        end_message = "END"
        ser.write(end_message.encode())
        break
