#include <Servo.h>

const int fullservoPin = 3;
const int halfservoPin = 5;
const int magnetPin = 7;
int magnetOnOff = 0; //off
int rotateAngle = 0; //forward heading
int extendAngle = 0; //unextended
int fullservoSpeed = 45; //**for continuous servo, varies from 1 to 90
int halfservoSpeed = 30; //it's the delay time
int CWSpeed = 90-fullservoSpeed;
int CCWSpeed = 90+fullservoSpeed; //90 is stationary
//from stack-exchange, T for 60 deg = (0.12 - 0.10) * (5.0 - 4.8) / (4.8 - 6.0) + 0.12 = 0.116667
                     //T for 10 deg = 0.01944
int TURN_TIME = 2*75.125; //milliseconds to turn 45 deg
Servo fullServo;// Creates a servo object for controlling the 360
Servo halfServo;// Creates a servo object for controlling the 180

void setup() {
  Serial.begin(9600);
  pinMode(magnetPin,OUTPUT);
  fullServo.attach(fullservoPin); // 900 min and 2100 max pulsewidth? https://store.arduino.cc/usa/feetech-continuous-rotation-micro-servo?queryID=2fae8d106efe5a06d30078d799350de2
  fullServo.write(90);
  halfServo.attach(halfservoPin);
  halfServo.write(0); //only need this if halfServo is used for extend
 
  // .write() syntax: stationary 0 is maxspd CW and 180 maxspd CCW
////according to https://arduino.stackexchange.com/questions/1321/servo-wont-stop-rotating
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString();// for checking
    Serial.print(data);// to show what's the key being pressed
    //delay(500);// for checking
    if (data == "Z\n") //extend magnet
      {
      extendAngle += 45;
      fullServo.write(CCWSpeed);
      delay(TURN_TIME);
      fullServo.write(90);
//      if (extendAngle > 359)
//        {extendAngle -= 359;
//        }
//      else if (extendAngle < 0)
//        {extendAngle += 359;
//        }
      Serial.println(extendAngle);  
      }
    else if (data == "X\n") //retract magnet
      {
      extendAngle -= 45;
      fullServo.write(CWSpeed);
      delay(TURN_TIME);
      fullServo.write(90);
//      if (extendAngle > 359)
//        {extendAngle -= 359;
//        }
//      else if (extendAngle < 0)
//        {extendAngle += 359;
//        }
      Serial.println(extendAngle);  
      }
    else if (data == "C\n" && rotateAngle <= 50) //rotate arm use 50 because of limited clearance on top of RVR
      {
      int startRotate = rotateAngle;
      for(int i = startRotate; i < 50; i += 2) 	 // command to move from 0 degrees to 180 degrees 
        {                                  
        halfServo.write(i); //command to rotate the servo to the specified angle
        delay(halfservoSpeed);
        rotateAngle = i;
        }
      Serial.println(rotateAngle);
      }
    else if (data == "V\n" && rotateAngle > 0) //return arm to original heading
      {
      int startReturn = rotateAngle;
      for(int i = startReturn; i > 0; i -= 2) 	 // command to move from 0 degrees to 180 degrees 
        {                                  
        halfServo.write(i); //command to rotate the servo to the specified angle
        delay(halfservoSpeed);
        rotateAngle = i;        
        }
      Serial.println(rotateAngle);
      }
    else if (data == "M\n") //toggle magnet on or off
      {
      if (magnetOnOff == 0)
        { digitalWrite(magnetPin, HIGH);
          magnetOnOff = 1;
          Serial.println("magnet On");
        }
      else if (magnetOnOff == 1)
        { digitalWrite(magnetPin, LOW);
          magnetOnOff = 0;
          Serial.println("magnet Off");
        }
      }
//    else if (data == "SPACE\n") //halt arm
//      {
//      halfServo.write(extendAngle);
//      delay(100); //randomly choose 100
//      }    
    else if (data == "ENTER\n") //keep and drive
      {
      returnArm();
      }
//    else {} //should do nothing if readString gives neither Z nor X
    delay(500);
  }
}

void returnArm() { 
  if (extendAngle > 0) // if angle < 0 then function is not run, since the user is likely to have done a manual retract
    {
    fullServo.write(CWSpeed);
    delay((extendAngle/45)*TURN_TIME);
    }
  fullServo.write(90);
  extendAngle = 0;
  for(int i = rotateAngle; i > 0; i -= 2) // command to move from 0 degrees to 180 degrees 
    {                                  
    halfServo.write(i); //command to rotate the servo to the specified angle
    delay(halfservoSpeed);
    rotateAngle = i;
    }    
  halfServo.write(0); //just a fail-safe to make sure it's returned
  Serial.println("Arm Returned");
  }
