#include <Servo.h>
Servo servo01;
Servo servo02;
Servo servo03;

Servo servo04;
Servo servo05;
Servo servo06;

Servo servo_list[6] = { servo01, servo02, servo03, servo04, servo05, servo06 };
int angle_list[6] = { 90, 90, 50, 90, 80, 90}; // 초기값과 같게

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

  servo_default();
  delay(1000);

  
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  servo_rotate(2, 45);
  delay(100);
  servo_rotate(3, 100);
  
  
}


void servo_default()
{
   servo01.write(angle_list[0]);
   servo02.write(angle_list[1]);
   servo03.write(angle_list[2]);
   servo04.write(angle_list[3]);
   servo05.write(angle_list[4]);
   servo06.write(angle_list[5]);
}

void attach_All_Pin()
{
  servo01.attach(pin_01);
  servo02.attach(pin_02);
  servo03.attach(pin_03);
  servo04.attach(pin_04);
  servo05.attach(pin_05);
  servo06.attach(pin_06);
}

void detach_All_Pin()
{
  servo01.detach();
  servo02.detach();
  servo03.detach();
  servo04.detach();
  servo05.detach();
  servo06.detach();
}

void servo_rotate(int servo_num, int angle)
{
  int idx  = servo_num - 1;
  int b4_ang = angle_list[idx];
  int target_ang = angle;
  int diff = target_ang - b4_ang;

  if(diff > 0)
  {
    for(int i = b4_ang; b4_ang + i <= target_ang; i++)
    {
      servo_list[idx].write(b4_ang + i);
      delay(100);
    }
  }
  else if(diff < 0)
  {
    for(int i = b4_ang; b4_ang - i >= target_ang; i++)
    {
      servo_list[idx].write(b4_ang - i);
      delay(100);
    }
  }
  angle_list[idx] = target_ang;
}
