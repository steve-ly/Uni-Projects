#include "scale.h"

//Constructor
Scale::Scale() {
//  Serial.println("Constructing Scale");
  _scale = new NAU7802();
}

bool Scale::isScaleAvailable() {
    return _scale->available();
}

float Scale::getCurrentReading() {
    return _scale->getReading();
}

float Scale::getCurrentWeight() {
    _currentWeight = _scale->getWeight(true, 50) - _holdOffset;
    if (_currentWeight < 0) _currentWeight = 0;
    return _currentWeight;
}

//float Scale::getCurrentWeight() {
//    return _currentWeight;
//}

void Scale::setHoldWeight() {
    _holdWeight = _currentWeight;
}

float Scale::getHoldWeight() {
    return _holdWeight;
}

void Scale::setHoldOffset() {
    _holdOffset = _scale->getWeight(true)- _holdWeight;
}

float Scale::getHoldOffset() {
    return _holdOffset;
}

void Scale::setZeroOffset() {
    _scale->calculateZeroOffset();
}

void Scale::detectScale() {
    if (_scale->begin() == false)
    {
        Serial.println("Scale not detected. Please check wiring. Freezing...");
        while (1);
    }
    Serial.println("Scale detected!");
}

void Scale::initScale() {
    readSystemSettings();
    _scale->setSampleRate(NAU7802_SPS_320); //Increase to max sample rate
    _scale->calibrateAFE(); //Re-cal analog front end when we change gain, sample rate, or channel 

    Serial.print("Zero offset: ");
    Serial.println(_scale->getZeroOffset());
    Serial.print("Calibration factor: ");
    Serial.println(_scale->getCalibrationFactor());
}

//Gives user the ability to set a known weight on the scale and calculate a calibration factor
void Scale::calibrateScale(void) {
    Serial.println();
    Serial.println();
    Serial.println(F("Scale calibration"));

    Serial.println(F("Setup scale with no weight on it. Press a key when ready."));
    while (Serial.available()) Serial.read(); //Clear anything in RX buffer
    while (Serial.available() == 0) delay(10); //Wait for user to press key

    _scale->calculateZeroOffset(64); //Zero or Tare the scale. Average over 64 readings.
    Serial.print(F("New zero offset: "));
    Serial.println(_scale->getZeroOffset());

    Serial.println(F("Place known weight on scale. Press a key when weight is in place and stable."));
    while (Serial.available()) Serial.read(); //Clear anything in RX buffer
    while (Serial.available() == 0) delay(10); //Wait for user to press key

    Serial.print(F("Please enter the weight, without units, currently sitting on the scale (for example '4.25'): "));
    while (Serial.available()) Serial.read(); //Clear anything in RX buffer
    while (Serial.available() == 0) delay(10); //Wait for user to press key

    //Read user input
    float weightOnScale = Serial.parseFloat();
    Serial.println();

    _scale->calculateCalibrationFactor(weightOnScale, 64); //Tell the library how much weight is currently on it
    Serial.print(F("New cal factor: "));
    Serial.println(_scale->getCalibrationFactor(), 2);

    Serial.print(F("New Scale Reading: "));
    Serial.println(_scale->getWeight(), 2);

    recordSystemSettings(); //Commit these values to EEPROM
}

//Record the current system settings to EEPROM
void Scale::recordSystemSettings(void) {
    //Get various values from the library and commit them to NVM
    EEPROM.put(LOCATION_CALIBRATION_FACTOR, _scale->getCalibrationFactor());
    EEPROM.put(LOCATION_ZERO_OFFSET, _scale->getZeroOffset());
}

//Reads the current system settings from EEPROM
//If anything looks weird, reset setting to default value
void Scale::readSystemSettings(void) {
    float settingCalibrationFactor; //Value used to convert the load cell reading to lbs or kg
    long settingZeroOffset; //Zero value that is found when scale is tared

    //Look up the calibration factor
    EEPROM.get(LOCATION_CALIBRATION_FACTOR, settingCalibrationFactor);
    if (settingCalibrationFactor == 0xFFFFFFFF)
    {
        settingCalibrationFactor = 0; //Default to 0
        EEPROM.put(LOCATION_CALIBRATION_FACTOR, settingCalibrationFactor);
    }

    //Look up the zero tare point
    EEPROM.get(LOCATION_ZERO_OFFSET, settingZeroOffset);
    if (settingZeroOffset == 0xFFFFFFFF)
    {
        settingZeroOffset = 1000L; //Default to 1000 so we don't get inf
        EEPROM.put(LOCATION_ZERO_OFFSET, settingZeroOffset);
    }

    //Pass these values to the library
    _scale->setCalibrationFactor(settingCalibrationFactor);
    _scale->setZeroOffset(settingZeroOffset);

    _settingsDetected = true; //Assume for the moment that there are good cal values
    if (settingCalibrationFactor < 0.1 || settingZeroOffset == 1000)
        _settingsDetected = false; //Defaults detected. Prompt user to cal scale.
}
