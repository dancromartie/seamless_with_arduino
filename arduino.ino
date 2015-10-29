#include <Process.h>

int sensorValue;

void setup() {
  Bridge.begin();
}

void sendLight(int lightVal) {
  Process p;           
  p.begin("curl");
  String url = "http://192.168.0.2:6789/seamless/send_light/";
  url += lightVal;
  p.addParameter(url);
  p.run();
  while (p.available()>0) {
    char c = p.read();
  }
}

void loop() {
  delay(1000);
  sensorValue = analogRead(A0);
  sendLight(sensorValue);
}
