#pragma once

#ifndef SMSTRUCTS_H
#define SMSTRUCTS_H

#using <System.dll>
#include <Windows.h>
#include <tchar.h>
#include <TlHelp32.h>
#include <stdio.h>
#include <iostream>
#include <conio.h>

using namespace System;
using namespace System::Net::Sockets;
using namespace System::Net;
using namespace System::Text;


#define STANDARD_LASER_LENGTH 361

struct SM_Laser
{
	double x[STANDARD_LASER_LENGTH];
	double y[STANDARD_LASER_LENGTH];
};

struct SM_VehicleControl
{
	double Speed;
	double Steering;
};

struct SM_GPS
{
	double Northing;
	double Easting;
	double Height;

};

struct UnitFlags
{
	unsigned char	Laser : 1,				//CRITICAL
					Camera : 1,				//CRITICAL
					VehicleControl : 1,		//CRITICAL
					Display : 1,				//NONCRITICAL
					GPS : 1,				//NONCRITICAL
					Garbage : 3;	
};
	
union ExecFlags
{
	UnitFlags Flags;
	unsigned short Status;
};

struct ProcessManagement
{
	ExecFlags Heartbeat;
	ExecFlags Shutdown;
	long int LifeCounter;
};

#define NONCRITICALMASK 0xff	//0 011 1000
#define CRITICALMASK 0x0		//0 000 0111
#endif
