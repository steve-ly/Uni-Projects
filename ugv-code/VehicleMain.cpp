
#using <System.dll>

#include <conio.h>//_kbhit()
#include <Windows.h>
#include "SMStructs.h"
#include "SMObject.h"
#include "Vehicle.h"

using namespace System;
using namespace System::Net::Sockets;
using namespace System::Net;
using namespace System::Text;

using namespace System::Diagnostics;
using namespace System::Threading;

int main()
{
	
	int waitTimeCounter = 0;
	Vehicle vehicle;
	vehicle.setupSharedMemory();
	vehicle.setHeartbeat(1);
	vehicle.connect("192.168.1.200", 25000);

	while (1) {
	
		System::Threading::Thread::Sleep(100);
		vehicle.getData();



		if (vehicle.getShutdownFlag() == 1) {
			break;
		}
		//heartbeat
		System::Threading::Thread::Sleep(400);
		if (vehicle.getHeartbeat() == 0) {
			waitTimeCounter = 0;
			vehicle.setHeartbeat(1);
		}
		else {
			waitTimeCounter++;
			if (vehicle.getHeartbeat() == 1) {
				if (waitTimeCounter > 15) {
					vehicle.setShutdownFlag();
				}
			}
		}
	}




	return 0;
}