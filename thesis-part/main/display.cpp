#include "display.h"

Display::Display() {
    _lcd = new LiquidCrystal_I2C(0x27, 16, 2);
}

void Display::initDisplay() {
    _lcd->init();
    _lcd->backlight();
}

void Display::printHoldWeight(float weight) {
    _lcd->setCursor(2,0);
    _lcd->print("Holding Weight:");
    _lcd->setCursor(2,1); 
    _lcd->print(weight, 3);
}

void Display::printCurrentWeight(float weight) {
    _lcd->setCursor(2,0);
    _lcd->print("Weight:          ");
    _lcd->setCursor(2,1);
    _lcd->print(weight, 3);
}
