#include <Wire.h>
#include <Pushbutton.h>

#include "scale.h"
#include "display.h"

Scale myScale;
Display myDisplay;

Pushbutton button(3);
Pushbutton buttonTare(2);

void setup()
{
    Serial.begin(9600);
    Serial.println("Starting...");

    Wire.begin();
//    Wire.setClock(400000); //Qwiic Scale is capable of running at 400kHz if desired
    Wire.setClock(5000); //Qwiic Scale is capable of running at 400kHz if desired

//    myScale = new Scale();
//    myDisplay = new Display();
    
    myScale.detectScale();
    myScale.initScale();

    myDisplay.initDisplay();
}

void loop()
{
    if (myScale.isScaleAvailable()) {
        
        Serial.print("Reading: ");
        Serial.print(myScale.getCurrentReading());
        Serial.print("\tWeight: ");
        Serial.print(myScale.getCurrentWeight(), 5); //Print 2 decimal places
        Serial.print("\tOffset:  ");
        Serial.print(myScale.getHoldOffset());

        // print out to liquiddisplay
        myDisplay.printCurrentWeight(myScale.getCurrentWeight());
        // delay(100);
        if (buttonTare.getSingleDebouncedPress()) {
            myScale.setZeroOffset();
            Serial.println(F("TARED"));   
        }
        
        if (button.getSingleDebouncedPress()){
            myScale.setHoldWeight();
            while(!button.getSingleDebouncedPress()) {
                myDisplay.printHoldWeight(myScale.getHoldWeight());
                myScale.setHoldOffset();
                // Serial.print("\tOffset");
                // Serial.print(holdoffset);
            }
        }
        
        if (myScale._settingsDetected == false) {
            // myScale.calculateZeroOffset(true);
        }

        Serial.println();
    }

    if (Serial.available())
    {
        byte incoming = Serial.read();
        if (incoming == 't') {
            //Tare the scale
            myScale.setZeroOffset();
        } else if (incoming == 'c') {
            //Calibrate 
            myScale.calibrateScale();
        }
    }
}
