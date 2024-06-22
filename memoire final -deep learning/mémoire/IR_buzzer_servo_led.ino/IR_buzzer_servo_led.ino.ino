/*
    1.  If an object is detected, turn the 
      servo motor 10 degrees
    2.  If there is no object detected, 
      turn the servo motor 150 degrees
  */

  #include <Servo.h>
  Servo Serv;
    
  int pinIR=2;
  int pinServo=4;
  int val=0;
  int led=3;
  int Buzzer=7;
  

  void setup(){
    Serv.attach(pinServo);
    pinMode(3, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(7, OUTPUT);
  }

  void loop(){
    val = digitalRead(pinIR);
  
    if (val ==0){
      digitalWrite(led,HIGH);
      delay(100);     
      Serv.write(150);
      tone (7, 600);
      delay(100);
    }
    else
    {
      Serv.write(10);  
      noTone(7);
      digitalWrite(led,LOW);
      delay(100);
    }
  }