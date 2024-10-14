#using <System.dll>

#include "Laser.h"


using namespace System;

using namespace System::Net::Sockets;
using namespace System::Net;
using namespace System::Text;


int Laser::connect(String^ hostName, int portNumber)
{
	//int PortNumber = 23000;

	// String to store received data for display

	// Creat TcpClient object and connect to it
	Client = gcnew TcpClient(hostName, portNumber);
	// Configure connection
	Client->NoDelay = true;
	Client->ReceiveTimeout = 500;//ms
	Client->SendTimeout = 500;//ms
	Client->ReceiveBufferSize = 1024;
	Client->SendBufferSize = 1024;
	// unsigned char arrays of 16 bytes each are created on managed heap
	SendData = gcnew array<unsigned char>(16);
	ReadData = gcnew array<unsigned char>(2500);
	String^ AskScan = gcnew String("5257127\n");
	SendData = System::Text::Encoding::ASCII->GetBytes(AskScan);

	// Get the network streab object associated with clien so we 
	// can use it to read and write
	Stream = Client->GetStream();
	Stream->Write(SendData, 0, SendData->Length);
	System::Threading::Thread::Sleep(1000);
	Stream->Read(ReadData, 0, ReadData->Length);
	String^ AuthStatus = System::Text::Encoding::ASCII->GetString(ReadData);
	Console::WriteLine(AuthStatus);

	AskScan = gcnew String("sRN LMDscandata");
	SendData = System::Text::Encoding::ASCII->GetBytes(AskScan);

	return 1;
}






int Laser::setupSharedMemory()
{
	ProcessManagementData = new SMObject(TEXT("ProcessManagement"), sizeof(ProcessManagement));
	ProcessManagementData->SMAccess();
	PMdata = (ProcessManagement*)ProcessManagementData->pData;
	if (ProcessManagementData->SMAccessError) {
		Console::WriteLine("Failed to access pm ");
		return 0;
	}

	SensorData = new SMObject(TEXT("SM_Laser"), sizeof(SM_Laser));
	SensorData->SMAccess();
	Sdata = (SM_Laser*)SensorData->pData;
	if (SensorData->SMAccessError) {
		Console::WriteLine("Failed to access lm ");
		return 0;
	}

	return 1;
}
int Laser::getData()
{
	// Write command asking for data
	Stream->WriteByte(0x02);
	Stream->Write(SendData, 0, SendData->Length);
	Stream->WriteByte(0x03);
	// Wait for the server to prepare the data, 1 ms would be sufficient, but used 10 ms
	System::Threading::Thread::Sleep(100);
	// Read the incoming data
	Stream->Read(ReadData, 0, ReadData->Length);
	// Convert incoming data from an array of unsigned char bytes to an ASCII string
	String^ Response;
	Response = System::Text::Encoding::ASCII->GetString(ReadData);
	ConvertedData = gcnew array<String^>(393);
	ConvertedData = Response->Split(' ');
	// Print the received string on the screen
	//Console::WriteLine(ConvertedData[23]);
	return 1;
}
int Laser::checkData()
{
	//check first string from readdata
	// YOUR CODE HERE
	if (ConvertedData[1] == "LMDscandata") {
		return 1;
	}
	else {
		return 0;
	}
}
int Laser::sendDataToSharedMemory()
{
	//Console::WriteLine("made here");
	double StartAngle = System::Convert::ToInt32(ConvertedData[23], 16);
	int NumRanges = System::Convert::ToInt32(ConvertedData[25], 16);
	Console::WriteLine("Num Ranges:" + NumRanges);
	array<double>^ Range = gcnew array<double>(361);
	//Console::WriteLine("made here2");
	double angle = 0;
	double PI = 3.141592653589793238462643383279502884;

	for (int i = 0; i < 361; i++) {
		Range[i] = System::Convert::ToInt32(ConvertedData[26 + i], 16);
		Sdata->y[i] = Range[i] * sin(angle * PI / 180);
		Sdata->x[i] = -Range[i] * cos(angle * PI / 180);

		Console::WriteLine("x: " + Sdata->x[i] + " y: " + Sdata->y[i] + "Angle: " + angle + "Number: " + i);
		angle = angle + 0.5;
	}
	Console::WriteLine("Next set of coords:");
	// YOUR CODE HERE
	return 1;
}
bool Laser::getShutdownFlag()
{
	// YOUR CODE HERE
	return (PMdata->Shutdown.Flags.Laser);
}
int Laser::setShutdownFlag()
{
	// YOUR CODE HERE
	PMdata->Shutdown.Flags.Laser = 1;
	return 1;
}
int Laser::getHeartbeat()
{

	return (PMdata->Heartbeat.Flags.Laser);
}
int Laser::setHeartbeat(bool heartbeat)
{
	PMdata->Heartbeat.Flags.Laser = heartbeat;
	return 1;
}
Laser::~Laser()
{
	// YOUR CODE HERE
	if (ProcessManagementData != NULL) {
		delete(ProcessManagementData);

	}
	if (SensorData != NULL) {
		delete(SensorData);

	}

}

