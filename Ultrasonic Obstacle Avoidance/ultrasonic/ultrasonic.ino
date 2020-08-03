const int trigPinLeft = 6;
const int echoPinLeft = 7;
const int trigPinRight = 8;
const int echoPinRight = 9;
long durationLeft;
long durationRight;
int distanceLeft;
int distanceRight;
int threshold = 35; // default 35, adjust according to sensor sensitivity



void setup() {
  pinMode(trigPinLeft, OUTPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(echoPinRight, INPUT);
  Serial.begin(9600);
}

void loop() {
  while (Serial.readString() != "END") {
    ////for debugging
    //Serial.print("Leftdist");
    //Serial.println(calculateDistanceLeft());
    //Serial.print("Rightdist");
    //Serial.println(calculateDistanceRight());
    while (calculateDistanceLeft() > threshold && calculateDistanceRight() > threshold) 
      { 
      Serial.println("Forward");
      delay(200);
      }
    
    if (calculateDistanceLeft() < threshold || calculateDistanceRight() < threshold)
      { 
      if (calculateDistanceLeft() > calculateDistanceRight())
        {Serial.println("Left");
         delay(300);
        }
      else if (calculateDistanceLeft() < calculateDistanceRight())
        {Serial.println("Right");
         delay(300);
        }
      }
    else {}
  }
}


// referenced from https://howtomechatronics.com/projects/arduino-radar-project/
int calculateDistanceLeft() {
  digitalWrite(trigPinLeft, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPinLeft, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPinLeft, LOW);
  durationLeft = pulseIn(echoPinLeft, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  distanceLeft= durationLeft*0.034/2;
  return distanceLeft;
}
int calculateDistanceRight() {
  digitalWrite(trigPinRight, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPinRight, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPinRight, LOW);
  durationRight = pulseIn(echoPinRight, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  distanceRight= durationRight*0.034/2;
  return distanceRight;
}
