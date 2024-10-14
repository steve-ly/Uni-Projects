#using <System.dll>

#include <conio.h>//_kbhit()
#include <Windows.h>
#include "SMStructs.h"
#include "SMObject.h"
#include "GPS.h"

using namespace System;
using namespace System::Net::Sockets;
using namespace System::Net;
using namespace System::Text;

using namespace System::Diagnostics;
using namespace System::Threading;

int main()
{
	
	int waitTimeCounter = 0;
	GPS gps;
	gps.setupSharedMemory();
	gps.setHeartbeat(1);

	//laser.setupSharedMemory();
	String^ ipAddresss = gcnew String("192.168.1.200");
	int port = 24000;

	if (!gps.setupSharedMemory()) {
		System::Threading::Thread::Sleep(5000);

		gps.setShutdownFlag();
	}
	gps.connect(ipAddresss, port);
	gps.setHeartbeat(1);

	while (1) {

		gps.getData();
		if (gps.getShutdownFlag() == 1) {
			break;
		}

		



		if (gps.checkData() != 1) {
			
			gps.setShutdownFlag();
			break;
		}
		gps.sendDataToSharedMemory();

		
		//heartbeat
		System::Threading::Thread::Sleep(200);
		if (gps.getHeartbeat() == 0) {
			waitTimeCounter = 0;
			gps.setHeartbeat(1);
		}
		else {
			waitTimeCounter++;
			if (gps.getHeartbeat() == 1) {
				if (waitTimeCounter > 10) {
					gps.setShutdownFlag();
				}
			}
		}
		

	}




	return 0;
}