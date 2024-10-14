#ifndef SCALE_H_
#define SCALE_H_

#include <EEPROM.h>
#include "Arduino.h"
#include "SparkFun_Qwiic_Scale_NAU7802_Arduino_Library.h"

//EEPROM locations to store 4-byte variables
#define LOCATION_CALIBRATION_FACTOR 0 //Float, requires 4 bytes of EEPROM
#define LOCATION_ZERO_OFFSET 10 //Must be more than 4 away from previous spot. Long, requires 4 bytes of EEPROM

class Scale
{
    public:
        Scale();

        /** 
         *  @brief return true if loadcell, 
         *  sparkfun chip and Arduino is correctly connect to each other 
         */ 
        bool isScaleAvailable();

        
        /**
         * @brief calcualte the weight from digital reading 
         * it is not accurate if scale is not calibrated yet
         * 
         */
//        void setCurrentWeight();
        float getCurrentWeight();

        /**
         * @brief get digital reading from sparkfun chip
         * 
         * @return float 
         */
        float getCurrentReading();

        /**
         * @brief hold the weight, at this moment, 
         * stop reading digital stream from chip
         */
        void setHoldWeight();
        float getHoldWeight();

        /**
         * @brief Set the Hold Offset object
         * 
         */
        void setHoldOffset();
        float getHoldOffset();

        /**
         * @brief Set zero offset 
         * 
         */
        void setZeroOffset();

        /**
         * @brief check whether the scale is connected
         * 
         */
        void detectScale();

        /**
         * @brief initiate scale
         * 
         */
        void initScale();

        /**
         * @brief rectify the scale by finding correct zero offset and scale factor
         * 
         */
        void calibrateScale(void);

        bool _settingsDetected = false;

    private:
        /**
         * @brief put system setting into EEPROM
         * (zero-offset and scale factor)
         */
        void recordSystemSettings(void);

        /**
         * @brief read system setting into EEPROM
         * (zero-offset and scale factor)
         */
        void readSystemSettings(void);
        NAU7802* _scale;

        float _currentReading;
        float _currentWeight;

        float _holdWeight = 0;
        float _holdOffset = 0;
};

#endif  // SCALE_H_
