#using <System.dll>
#include <Windows.h>
#include <tchar.h>
#include <TlHelp32.h>
#include <stdio.h>
#include <iostream>
#include <conio.h>
#include <signal.h>
#include "SMStructs.h"
#include "SMObject.h"

using namespace System;
using namespace System::Text;
using namespace System::Diagnostics;
using namespace System::Threading;



int main() {
	//"Laser.exe","Camera","Vehicle","Display","GPS.exe" 
	array<String^>^ ModuleList = gcnew array<String^>{"Laser.exe", "Camera.exe", "Vehicle.exe", "Display.exe", "GPS.exe" };
	array<int>^ Critical = gcnew array<int>(ModuleList->Length) { 1, 1, 1, 0, 0 };
	array<int>^ ProcessCounter = gcnew array<int>(ModuleList->Length);
	array<int>^ CrashLimit = gcnew array<int>(ModuleList->Length) { 4, 4, 4, 4, 4 };
	array<char>^ PrintHeartBeat = gcnew array<char>(ModuleList->Length) { '0', '0', '0', '0', '0' };


	array<Process^>^ ProcessList = gcnew array<Process^>(ModuleList->Length);

	SMObject PMObj(TEXT("ProcessManagement"), sizeof(ProcessManagement));
	PMObj.SMCreate();
	PMObj.SMAccess();
	if (PMObj.SMCreateError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}
	if (PMObj.SMAccessError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}
	ProcessManagement* PMData = (ProcessManagement*)PMObj.pData;



	SMObject LaserObj(TEXT("SM_Laser"), sizeof(SM_Laser));
	LaserObj.SMCreate();
	LaserObj.SMAccess();
	if (LaserObj.SMCreateError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}
	if (LaserObj.SMAccessError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}

	SMObject GPSObj(TEXT("SM_GPS"), sizeof(SM_GPS));
	GPSObj.SMCreate();
	GPSObj.SMAccess();
	if (GPSObj.SMCreateError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}
	if (GPSObj.SMAccessError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}
	

	SMObject VehicleObj(TEXT("SM_VehicleControl"), sizeof(SM_VehicleControl));
	VehicleObj.SMCreate();
	VehicleObj.SMAccess();
	if (VehicleObj.SMCreateError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}
	if (VehicleObj.SMAccessError) {
		Console::WriteLine("Unable to create share memory, shutting down ProcessManagement");
		System::Threading::Thread::Sleep(2000);
		return 1;
	}



	for (int i = 0; i < 5; i++) {
		if (Process::GetProcessesByName(ModuleList[i])->Length == 0) {
			ProcessList[i] = gcnew Process;
			ProcessList[i]->StartInfo->FileName = ModuleList[i];
			ProcessList[i]->Start();
			Console::WriteLine("The Process" + ModuleList[i] + ".exe started");
		}
	}
	int mask = 0x01;
	System::Threading::Thread::Sleep(2000); //wait for everything to load

	while (!_kbhit()) {
		/*	if (kbhit()) {
				char c = getch();
				if ((const char*)toupper(c) == "Q") {
					break;
				}
			}
			*/

		if (PMData->Shutdown.Status) {
			break;
		}
		//Heartbeat check
		//PMData->Heartbeat
		
		for (int i = 0; i < 5; i++) {
			int bit = (PMData->Heartbeat.Status >> i) & 1;
			PrintHeartBeat[i] = bit;

			System::Threading::Thread::Sleep(200);
			if (bit == 1) {
				PMData->Heartbeat.Status = PMData->Heartbeat.Status ^ (mask << i);
				ProcessCounter[i] = 0;
			}
			else {
				ProcessCounter[i]++;
				if (ProcessCounter[i] > CrashLimit[i]) {
					if (Critical[i] == 1) {
						PMData->Shutdown.Status = 0xFF;
						Console::WriteLine("Critical Process" + ModuleList[i] + "has failed, shutting down");
						break;

					}
					else {
						ProcessCounter[i]++;
						if (ProcessList[i]->HasExited) {
							ProcessList[i]->Start();
						}
						else {
							ProcessList[i]->Kill();
							ProcessList[i]->Start();
						}
					}
				}
			}
		}
	

		Console::WriteLine(" " + PrintHeartBeat[0] + " " + PrintHeartBeat[1] + " " + PrintHeartBeat[2] + " " + PrintHeartBeat[3] + " " + PrintHeartBeat[4] + " ");




	}
	
	Console::WriteLine("Performing Routine Shutdown");
	System::Threading::Thread::Sleep(200);

	for (int i = 0; i < 5; i++) {
		if (!ProcessList[i]->HasExited){
			Console::WriteLine("ShuttingDown" + ProcessList[i]);
			ProcessList[i]->Kill();

		}
		System::Threading::Thread::Sleep(200);

	}
	





	return 0;
}
