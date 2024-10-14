
#include "GPS.h"

int GPS::connect(String^ hostName, int portNumber) 
{
	// YOUR CODE HERE
	Client = gcnew TcpClient(hostName, portNumber);
	// Configure connection
	Client->NoDelay = true;
	Client->ReceiveTimeout = 500;//ms
	Client->SendTimeout = 500;//ms
	Client->ReceiveBufferSize = 1024;
	Client->SendBufferSize = 1024;
	// unsigned char arrays of 16 bytes each are created on managed heap
	SendData = gcnew array<unsigned char>(16);
	ReadData = gcnew array<unsigned char>(250);

	// Get the network streab object associated with clien so we 
	// can use it to read and write

	return 1;
}
int GPS::setupSharedMemory()
{
	// YOUR CODE HERE
	ProcessManagementData = new SMObject(TEXT("ProcessManagement"), sizeof(ProcessManagement));
	ProcessManagementData->SMAccess();
	PMdata = (ProcessManagement*)ProcessManagementData->pData;
	if (ProcessManagementData->SMAccessError) {
		Console::WriteLine("Failed to access pm ");
		return 0;
	}
	SensorData = new SMObject(TEXT("SM_GPS"), sizeof(SM_GPS));
	SensorData->SMAccess();
	Gdata = (SM_GPS*)SensorData->pData;
	if (SensorData->SMAccessError) {
		Console::WriteLine("Failed to access Gps memory ");
		return 0;
	}

	return 1;
}
int GPS::getData()
{
	// YOUR CODE HERE
	// Wait for the server to prepare the data, 1 ms would be sufficient, but used 10 ms
	// Read the incoming data
	Stream = Client->GetStream();
	System::Threading::Thread::Sleep(1000);
	if (Stream->DataAvailable) {
		Stream->Read(ReadData, 0, ReadData->Length);
	}


	NovatelGps = new GPSData;
	BytePtr = (unsigned char*)NovatelGps;
	unsigned int Header = 0;
	unsigned char Data;
	int i = 0;
	int Start; //Start of data
	while (Header != 0xaa44121c) {
		Data = ReadData[i++];
		Header = ((Header << 8) | Data);
	}

	if (Header == 0xaa44121c) {
		for (int i = 0; i < 112; i++)
		{
			*(BytePtr + i) = ReadData[i];
			//Buffer[i] = ReadData[i];

		}
	}
	//SendData = System::Text::Encoding::ASCII->GetBytes(ReadData);
	return 1;
}
int GPS::checkData()
{
	// YOUR CODE HERE

	unsigned long length = 108;
	Console::WriteLine("CRC is" + CalculateBlockCRC32(length, BytePtr));
	if (CalculateBlockCRC32(length, BytePtr) != NovatelGps->Checksum) {
		System::Threading::Thread::Sleep(200);
		return 0;
	}
	
	return 1;
}
int GPS::sendDataToSharedMemory()
{
	
	// YOUR CODE HERE
	Gdata->Northing = NovatelGps->Northing;
	Gdata->Easting = NovatelGps->Easting;
	Gdata->Height = NovatelGps->Height;

	Console::WriteLine("Northing: " + Gdata->Northing);
	Console::WriteLine("Easting: " + Gdata->Easting);
	Console::WriteLine("Height: " + Gdata->Height);

	//System::Threading::Thread::Sleep(100);


	return 1;
}
bool GPS::getShutdownFlag()
{
	// YOUR CODE HERE
	return (PMdata->Shutdown.Flags.GPS);
}
int GPS::setShutdownFlag()
{
	// YOUR CODE HERE
	PMdata->Shutdown.Flags.GPS = 1;

	return 1;
}
int GPS::getHeartbeat() {
	return (PMdata->Heartbeat.Flags.GPS);
}
int GPS::setHeartbeat(bool heartbeat)
{
	// YOUR CODE HERE
	PMdata->Heartbeat.Flags.GPS = heartbeat;

	return 1;
}
GPS::~GPS()
{
	// YOUR CODE HERE
	if (ProcessManagementData != NULL) {
		delete(ProcessManagementData);

	}
	if (SensorData != NULL) {
		delete(SensorData);

	}
	if (NovatelGps != NULL) {
		delete(NovatelGps);

	}
}

unsigned long CRC32Value(int i)
{
	int j;
	unsigned long ulCRC;
	ulCRC = i;
	for (j = 8; j > 0; j--)
	{
		if (ulCRC & 1)
			ulCRC = (ulCRC >> 1) ^ CRC32_POLYNOMIAL;
		else
			ulCRC >>= 1;
	}
	return ulCRC;
}

unsigned long CalculateBlockCRC32(unsigned long ulCount, /* Number of bytes in the data block */
unsigned char* ucBuffer) /* Data block */
{
	unsigned long ulTemp1;
	unsigned long ulTemp2;
	unsigned long ulCRC = 0;
	while (ulCount-- != 0)
	{
		ulTemp1 = (ulCRC >> 8) & 0x00FFFFFFL;
		ulTemp2 = CRC32Value(((int)ulCRC ^ *ucBuffer++) & 0xff);
		ulCRC = ulTemp1 ^ ulTemp2;
	}
	return(ulCRC);
}
