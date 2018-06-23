#include <SoftwareSerial.h>
#include "DumbServer.h"

/* The WiFi shield is connected to
 * the Arduino pins 3 and 2, as the
 * Arduino has only one hardware serial
 * port (pins 0 and 1) we are using a
 * serial port emulated in software. */
SoftwareSerial esp_serial(3, 2);
EspServer esp_server;

//Globale Variablen : 
int rgb_r = 0;
int rgb_g = 0;
int rgb_b = 0;
int alarm = 0;
//Pin Variablen
int pirPin = 4;
int buzzerPin = 9;
int RPin = 5;
int GPin = 11;
int BPin = 10;

void setup()
{
  Serial.begin(9600);
  esp_serial.begin(9600);

  pinMode(pirPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(RPin, OUTPUT);
  pinMode(GPin, OUTPUT);
  pinMode(BPin, OUTPUT);

  /* Connect to the wireless network with the name "GDI"
   * and password "password", change these to match
   * your wifi settings.
   *
   * If anything fails begin() will not return.
   *
   * To debug possible problems you can flash a second
   * Arduino with the "Bare Minimum" example,
   * connect the GNDs of the two Arduinos,
   * connect pin 3 or 2 of the Arduino with the Wifi-shield
   * to pin 1(TX) of the other Arduino and use the Serial monitor
   * to see the Wifi commands and error-messages. */
  Serial.println("Starting server...");
  esp_server.begin(&esp_serial, "Freewlan", "okan1234", 30303);
  Serial.println("...server is running");


  /* Get and print the IP-Address the python program
   * should connect to */
  char ip[16];
  esp_server.my_ip(ip, 16);

  Serial.print("My ip: ");
  Serial.println(ip);
}

void loop(){
  if(esp_server.available()) {
    String command= esp_server.readStringUntil('\n');
      if(command == "rgb"){
        rgb_r = esp_server.readStringUntil('\n').toInt();
        rgb_g = esp_server.readStringUntil('\n').toInt();
        rgb_b = esp_server.readStringUntil('\n').toInt();
        Serial.println(rgb_r);
        Serial.println(rgb_g);
        Serial.println(rgb_b);
        setRGB(rgb_r,rgb_g,rgb_b);
      }
      if(command == "alarm"){
        Serial.println(command);
        String alarm_handler = esp_server.readStringUntil('\n');
        Serial.println(alarm_handler);
        if(alarm_handler == "on"){
          alarm= 1;
        }else if(alarm_handler == "off"){
          alarm= 0; 
        }
      }
  }
  if(alarm == 1){
    Serial.println("in alarm drin  ");
    Serial.println(alarm);
    int alarm_status = digitalRead(pirPin);
    if(alarm_status == 1){
      alarm= 2;
      esp_server.println("alarm");
      Serial.println("alarm ausschlag");
    }
  }

  if(alarm == 2){
    Serial.println(alarm);
    Serial.println("es piept");
    tone(buzzerPin, 1000);
    delay(100);
    noTone(buzzerPin);
  }
}

void setRGB(int redValue, int greenValue, int blueValue) {
  analogWrite(RPin, redValue);
  analogWrite(GPin, greenValue);
  analogWrite(BPin, blueValue);
}

