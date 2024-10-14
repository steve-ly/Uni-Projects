
#include <UGV_module.h>
#include <iostream>

#include <smstructs.h>
#include <SMObject.h>
#include <SMFcn.h>
#using <System.dll>

using namespace System;

using namespace System::Net::Sockets;
using namespace System::Net;
using namespace System::Text;


ref class Laser : public UGV_module
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
	~Laser();

	void getError()
	{
		switch (Error)
		{
		case SUCCESS:
			std::cout << "Success." << std::endl;
			break;
		case ERR_NO_DATA:
			std::cout << "ERROR: No Data Available." << std::endl;
			break;
		case ERR_INVALID_DATA:
			std::cout << "ERROR: Invalid Data Received." << std::endl;
			break;
		}
	}





protected:
	// YOUR CODE HERE (ADDITIONAL MEMBER VARIABLES THAT YOU MAY WANT TO ADD)
	
	array<String^>^ ConvertedData;
	String^ ResponseData;


	SM_Laser* Sdata;


	//unsigned char* Buffer;


};
#pragma once