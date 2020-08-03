PARTS
I used 2 servo motors:
- EF92A (180 degree) micro:servo
- FEETECH (Fitec) FS90R Continuous Rotation Servo (9g) >> https://www.addicore.com/FS90R-Servo-p/ad314.htm
in the making of this servo arm, as the Arduino code suggests, I used the 180 servo at the base of the arm for ROTATION and the 360 one for EXTENDING/RETRACTING the magnet.
Lego parts used were taken mainly from the Technic 8295 set "Telescopic Handler". 
However, any parts can be used, as long as there are 2 Gears, one that's directly attached to the continuous motor and another that's attached to the spool.


LIMITATIONS of the code
1. rotates to the extremes of left and right using C & V keys, independent of keypress duration (which is more intuitive)
2. extends/retracts magnet by a fixed amount on each command, likewise independent of keypress duration
3. servoarm.py MUST be run via Terminal on the RPi (I had python3.7)
4. Can't drive and operate the arm simultaneously to protect the arm, hence "servo"/ "drive" modes are implemented. For a prototype that's made of something more robust that Lego, this may not be necessary.


FYI
The script servoarm.py is based off the Keyboard Control script at: https://sdk.sphero.com/docs/samples_content/raspberry_pi/python/keyboard_control_sample/
It may be worth looking up "Asynchronous programming" for a better understanding of the Sphero SDK library.