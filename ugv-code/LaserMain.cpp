//Compile in a C++ CLR empty project
#using <System.dll>

#include <conio.h>//_kbhit()
#include <Windows.h>
#include "SMStructs.h"
#include "SMObject.h"
#include "Laser.h"

using namespace System;
using namespace System::Net::Sockets;
using namespace System::Net;
using namespace System::Text;

using namespace System::Diagnostics;
using namespace System::Threading;



int main()
{

	Laser laser;
	//laser.setupSharedMemory();
	String^ ipAddresss = gcnew String("192.168.1.200");
	int port = 23000;

	if (!laser.setupSharedMemory()) {
		System::Threading::Thread::Sleep(50000);

		laser.setShutdownFlag();
	}
	laser.connect(ipAddresss, port);
	int waitTimeCounter = 0;
	laser.setHeartbeat(1);

	while (1) {
		if (laser.getShutdownFlag() == 1) {
			break;
		}
		laser.getData();

		if (laser.checkData() != 1){
			laser.setShutdownFlag();
			break;
		}
		laser.sendDataToSharedMemory();
		//heartbeat
		System::Threading::Thread::Sleep(200);
		if (laser.getHeartbeat() == 0) {
			waitTimeCounter = 0;
			laser.setHeartbeat(1);
		}
		else {
			waitTimeCounter++;
			if (laser.getHeartbeat() == 1) {
				if (waitTimeCounter > 15) {
					laser.setShutdownFlag();
				}
			}
		}


	}




	return 0;
}