#ifndef DISPLAY_H_
#define DISPLAY_H_

#include <LiquidCrystal_I2C.h>
#include "Arduino.h"

class Display
{
    public:
        Display();

        /** init liquid crystal, clear the output  */
        void initDisplay();

        void printHoldWeight(float weight);
        void printCurrentWeight(float weight);
        
    private:
        LiquidCrystal_I2C* _lcd;
};

#endif // DISPLAY_H_
