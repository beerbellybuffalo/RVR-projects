based off the Ultrasonic RVR code from: https://sdk.sphero.com/docs/samples_content/raspberry_pi/python/ultrasonic_rvr_sample/

Although the sample from above only uses the RPi and not together with the Arduino.
The goal is for the RVR to avoid obstacles indefinitely on its own, however this is hardly possible with only 2 ultrasonic proximity sensors.

Potential angles for future exploration: 
- attaching an ultrasonic sensor to a servo to scan the RVR's surroundings and identify an obstacle-free path of travel.
- mount sensors to "bumpers" at both the front and back, so that RVR won't get stuck
- sideways sensors? 