#include <Servo.h>
Servo servo01;
Servo servo02;
Servo servo03;

Servo servo04;
Servo servo05;
Servo servo06;

int pin_01 = 3;
int pin_02 = 5;
int pin_03 = 6;

int pin_04 = 9;
int pin_05 = 10;
int pin_06 = 11;

char angle;
String anlgle_s;
int angle_int;

void setup() {
  // put your setup code here, to run once:
  servo01.attach(pin_01);
  servo02.attach(pin_02);
  servo03.attach(pin_03);
  servo04.attach(pin_04);
  servo05.attach(pin_05);
  servo06.attach(pin_06);
  
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
//

//
   servo01.write(120);
   servo02.write(30);
   servo03.write(50);
   servo04.write(0);
   servo05.write(80);
   servo06.write(30);



}
