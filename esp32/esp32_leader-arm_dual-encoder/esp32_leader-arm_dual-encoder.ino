#include <Wire.h>
#include "MT6701.hpp"

// Wiring (MT6701 -> ESP32):
//  encoder 1: 
//    SDA -> D21
//    SCL -> D22
//  encoder 2: 
//    SDA -> D19
//    SCL -> D18


// ENCODERS --------------------------------------------------
TwoWire I2C_enc1 = TwoWire(0);
TwoWire I2C_enc2 = TwoWire(1);

MT6701 enc1;
MT6701 enc2;


// SCRIPT ----------------------------------------------------
void setup() {
    Serial.begin(115200);

    I2C_enc1.begin(21, 22, 400000);
    I2C_enc2.begin(19, 18, 400000);
    delay(128);

    enc1.begin(&I2C_enc1);
    enc2.begin(&I2C_enc2);
}


void loop() {
    float enc1_degrees = enc1.getAngleDegrees();
    float enc2_degrees = enc2.getAngleDegrees();

    Serial.print("enc1: ");
    Serial.print(enc1_degrees);
    Serial.print(", enc2: ");
    Serial.println(enc2_degrees);

    delay(64);
}
