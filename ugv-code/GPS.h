#include <UGV_module.h>
#include <iostream>

#include <smstructs.h>
#include <SMObject.h>
#include <SMFcn.h>
#using <System.dll>
#define CRC32_POLYNOMIAL 0xEDB88320L


unsigned long CRC32Value(int i);
unsigned long CalculateBlockCRC32(unsigned long ulCount, unsigned char* ucBuffer);
#pragma pack(1)

struct GPSData
{
	unsigned int Header;
	unsigned char Discards1[40];
	double Northing;
	double Easting;
	double Height;
	unsigned char Discards2[40];
	unsigned int Checksum;
};

ref class GPS : public UGV_module
{

public:
	int connect(String^ hostName, int portNumber) override;
	int setupSharedMemory() override;
	int getData() override;	
	int checkData() override;
	int sendDataToSharedMemory() override;
	bool getShutdownFlag() override;
	int setShutdownFlag() override;
	int getHeartbeat() override;
	int setHeartbeat(bool heartbeat) override;
	~GPS();


protected:
	// YOUR CODE HERE (ADDITIONAL MEMBER VARIABLES THAT YOU MAY WANT TO ADD)

	SM_GPS* Gdata;
	unsigned char* BytePtr;
	GPSData *NovatelGps;

};
#pragma once