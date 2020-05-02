#include <Servo.h>
#include "SR04.h"
#define TRIG_PIN 12
#define ECHO_PIN 11

Servo myservo;  // create servo object to control a servo
int pos = 90;    // variable to store the servo position

SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a;
 
void setup() {
        Serial.begin(9600); 
        myservo.attach(9); //Servo connected to D9
        delay(1000);
}
 
void loop() {
        a=sr04.Distance();
        Serial.println(a);
        //Serial.println("cm");
        // send data only when you receive data:
        while (Serial.available() > 0) {
                // read the incoming byte:
                int c = Serial.read();
                delay(2); 
                // say what you got:
                myservo.write(c);
        }
        delay(400);
}
