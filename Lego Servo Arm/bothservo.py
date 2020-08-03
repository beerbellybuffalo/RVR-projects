import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
##important! the '../' portion depends on where the code is stored! ../../ means the script only needs to check for imports up to 2 levels deeper than its location
##For more info on this line of code>> https://stackoverflow.com/questions/21005822/what-does-os-path-abspathos-path-joinos-path-dirname-file-os-path-pardir

import asyncio

from helper_keyboard_input import KeyboardHelper
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync

#to communicate with Arduino
import serial
ser=serial.Serial("/dev/ttyUSB0",9600) #USB0 is the Arduino here, change if necessary
ser.baudrate=9600


# initialize global variables
key_helper = KeyboardHelper()
current_key_code = -1
driving_keys = [119, 97, 115, 100, 109, 32, 10, -1] #W A S D M SPACE ENTER
servo_keys = [122, 120, 99, 118, 109, 32, 10, -1] #Z X C V M SPACE ENTER
speed = 0
heading = 0
flags = 0
max_speed = 75 #capped at 75 so as not to risk the arm falling off
mode = "drive" #can toggle to "servo" later

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

def keycode_callback(keycode):
    global current_key_code
    current_key_code = keycode
    print("Key code updated: ", str(current_key_code))


async def main():
    
    """
    Runs the main control loop for this demo.  Uses the KeyboardHelper class to read a keypress from the terminal.

    W - Go forward.  Press multiple times to increase speed.
    A - Decrease heading by -10 degrees with each key press.
    S - Go reverse. Press multiple times to increase speed.
    D - Increase heading by +10 degrees with each key press.
    Spacebar - Drive mode: Reset speed and flags to 0. RVR will coast to a stop
             - Servo mode: Stop Extension/Retraction
    Enter - Toggle Drive mode / Servo mode
    Z - Rotates Arm anticlockwise
    X - Rotates Arm clockwise
    C - Extend Arm
    V - Retract Arm
    M - Magnet On/Off
    """
    global current_key_code
    global speed
    global heading
    global flags
    global max_speed
    global mode
    global driving_keys
    global servo_keys
    await rvr.wake()

    await rvr.reset_yaw()

    while True:
        if mode == "drive":    
            if current_key_code == 119:  # W
                # if previously going reverse, reset speed back to 64
                if flags == 1:
                    speed = 25
                else:
                    # else increase speed
                    speed += 25
                # go forward
                flags = 0
            elif current_key_code == 97:  # A
                heading -= 10
            elif current_key_code == 115:  # S
                # if previously going forward, reset speed back to 64
                if flags == 0:
                    speed = 25
                else:
                    # else increase speed
                    speed += 25
                # go reverse
                flags = 1
            elif current_key_code == 100:  # D
                heading += 10
            elif current_key_code == 109:  # M
                ser.write("M\n".encode())
                await asyncio.sleep(0.3)
                print(ser.readline().decode().rstrip())
                print(ser.readline().decode().rstrip())
            elif current_key_code == 32:  # SPACE
                # reset speed and flags, but don't modify heading.
                speed = 0
                flags = 0
            elif current_key_code == 10: # ENTER
                mode = "servo"
                print ("current mode: ", mode)
                #we want the RVR stationary in servo mode
                speed = 0
                flags = 0
            elif current_key_code not in driving_keys:
                print(main.__doc__) #look up docstrings    
            # check the speed value, and wrap as necessary.
            if speed > max_speed: #defined above
                speed = max_speed
            elif speed < -max_speed:
                speed = -max_speed

            # check the heading value, and wrap as necessary.
            if heading > 359:
                heading = heading - 359
            elif heading < 0:
                heading = 359 + heading
            # reset the key code every loop
            current_key_code = -1

            # issue the driving command
            await rvr.drive_with_heading(speed, heading, flags)

            # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
            await asyncio.sleep(0.1)
        elif mode == "servo":
            if current_key_code == 122: # Z
                ser.write("Z\n".encode())
                await asyncio.sleep(0.3) #give time to update servoAngle in arduino code
                print(ser.readline().decode().rstrip()) #print the letter
                print(ser.readline().decode().rstrip()) #print angle
            elif current_key_code == 120: # X
                ser.write("X\n".encode())
                await asyncio.sleep(0.3)
                print(ser.readline().decode().rstrip())
                print(ser.readline().decode().rstrip())                
            elif current_key_code == 99: # C
                ser.write("C\n".encode())
                print(ser.readline().decode().rstrip())
#                 for i in range(10):
#                     if current_key_code == 32:
#                         ser.write("SPACE\n".encode())
#                         print(ser.readline().decode().rstrip()) #print SPACE
#                         break
#                     else:    
#                         await asyncio.sleep(0.1)
                await asyncio.sleep(0.5)
                print(ser.readline().decode().rstrip()) #print extendAngle
            elif current_key_code == 118: # V
                ser.write("V\n".encode())
                print(ser.readline().decode().rstrip())
#                 for i in range(10):
#                     if current_key_code == 32:
#                         ser.write("SPACE\n".encode())
#                         print(ser.readline().decode().rstrip())
#                         break
#                     else:    
#                         await asyncio.sleep(0.1)
                await asyncio.sleep(0.3)
                print(ser.readline().decode().rstrip())
            elif current_key_code == 109:  # M
                ser.write("M\n".encode())
                await asyncio.sleep(0.3)
                print(ser.readline().decode().rstrip())
                print(ser.readline().decode().rstrip())
#            elif current_key_code == 32:  # SPACE
#                 ser.write("SPACE\n".encode())
#                 await asyncio.sleep(0.3)
#                 print(ser.readline().decode().rstrip()) #confirm that space was registered
            elif current_key_code == 10: # ENTER
                ser.write("ENTER\n".encode())
                await asyncio.sleep(0.4) # give time for returnarm
                #ser.reset_input_buffer()
                #ser.reset_output_buffer()
                print(ser.readline().decode().rstrip())
                print(ser.readline().decode().rstrip())
                mode = "drive"
                print ("current mode: ", mode)
            elif current_key_code not in servo_keys:
                print(main.__doc__)
            # reset the key code every loop
            current_key_code = -1

            # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
            await asyncio.sleep(0.1)


def run_loop():
    global loop
    global key_helper
    key_helper.set_callback(keycode_callback)
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )


if __name__ == "__main__":
    loop.run_in_executor(None, key_helper.get_key_continuous)
    try:
        run_loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
        key_helper.end_get_key_continuous()
    finally:
        print("Press any key to exit.")
        exit(1)
