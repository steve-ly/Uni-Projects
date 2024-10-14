#include "Vehicle.h"

int Vehicle::connect(String^ hostName, int portNumber)
{
	// YOUR CODE HERE	
	// String to store received data for display

	// Creat TcpClient object and connect to it
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
	SendData = gcnew array<unsigned char>(50);
	array<unsigned char>^ SendAuth;
	SendAuth = gcnew array<unsigned char>(16);

	ReadData = gcnew array<unsigned char>(2500);
	String^ AskScan = gcnew String("5257127\n");
	SendAuth = System::Text::Encoding::ASCII->GetBytes(AskScan);

	// Get the network streab object associated with clien so we 
	// can use it to read and write
	Stream = Client->GetStream();
	Stream->Write(SendAuth, 0, SendAuth->Length);
	System::Threading::Thread::Sleep(1000);
	/*Stream->Read(ReadData, 0, ReadData->Length);
	String^ AuthStatus = System::Text::Encoding::ASCII->GetString(ReadData);
	Console::WriteLine(AuthStatus);*/

	return 1;
}
int Vehicle::setupSharedMemory()
{
	// YOUR CODE HERE
		// YOUR CODE HERE
	ProcessManagementData = new SMObject(TEXT("ProcessManagement"), sizeof(ProcessManagement));
	ProcessManagementData->SMAccess();
	PMdata = (ProcessManagement*)ProcessManagementData->pData;
	if (ProcessManagementData->SMAccessError) {
		Console::WriteLine("Failed to access pm ");
		return 0;
	}

	SensorData = new SMObject(TEXT("SM_VehicleControl"), sizeof(SM_VehicleControl));
	SensorData->SMAccess();
	Vdata = (SM_VehicleControl*)SensorData->pData;
	if (SensorData->SMAccessError) {
		Console::WriteLine("Failed to access lm ");
		return 0;
	}
	Flag = 0;

	return 1;
}
int Vehicle::getData()
{
	
	// YOUR CODE HERE
	if (Flag == 0) {
		Flag = 1;
	}
	else if (Flag == 1) {
		Flag = 0;
	}
	String^ SendControl = gcnew String("# " + Vdata->Steering.ToString("f2") + " " + Vdata->Speed.ToString("f2") + " " + Flag + " #");
	SendData = System::Text::Encoding::ASCII->GetBytes(SendControl);
	Stream->Write(SendData, 0, SendData->Length);
	System::Threading::Thread::Sleep(100);
	// Read the incoming data
	// Convert incoming data from an array of unsigned char bytes to an ASCII string

	// Print the received string on the screen
	//Console::WriteLine(ConvertedData[23]);
	Console::WriteLine(SendControl);
	Console::WriteLine("Steering: " + Vdata->Steering);
	Console::WriteLine("Speed: " + Vdata->Speed);
	Console::WriteLine("Flags: " + Flag);
	
	return 1;
}
int Vehicle::checkData()
{
	// YOUR CODE HERE
	return 1;
}
int Vehicle::sendDataToSharedMemory()
{
	// YOUR CODE HERE
	return 1;
}
bool Vehicle::getShutdownFlag()
{
	// YOUR CODE HERE
	return (PMdata->Shutdown.Flags.VehicleControl);
}
int Vehicle::setShutdownFlag()
{
	// YOUR CODE HERE
	PMdata->Shutdown.Flags.VehicleControl = 1;

	return 1;
}
int Vehicle::getHeartbeat() {
	return (PMdata->Heartbeat.Flags.VehicleControl);
}
int Vehicle::setHeartbeat(bool heartbeat)
{
	// YOUR CODE HERE
	PMdata->Heartbeat.Flags.VehicleControl = heartbeat;

	return 1;
}
Vehicle::~Vehicle()
{
	// YOUR CODE HERE
	if (ProcessManagementData != NULL) {
		delete(ProcessManagementData);

	}
	if (SensorData != NULL) {
		delete(SensorData);

	}
}
