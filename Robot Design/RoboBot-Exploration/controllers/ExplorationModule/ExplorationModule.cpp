// File:          my_controller.cpp
// Date:
// Description:
// Author:
// Modifications:

// You may need to add webots include files such as
// <webots/DistanceSensor.hpp>, <webots/Motor.hpp>, etc.
// and/or to add some other includes
#include <webots/Robot.hpp>

// All the webots classes are defined in the "webots" namespace
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_set>
#include <algorithm>
#include <utility>
#include <map>
#include <queue>
#include <limits>
#include <cstring>
#include <array>
#include <Windows.h>
#include<bits/stdc++.h>

#include <cmath>
#include <iomanip>
#include <memory>
#include <unistd.h>
#include <fstream>

#include <webots/Robot.hpp>
#include <webots/Motor.hpp>
#include <webots/DistanceSensor.hpp>
#include <webots/Keyboard.hpp>
//#include "my_controller.hpp"
//#include "phaseA.hpp"
//#define NV 45
#define ROWS 5
#define COLS 9
#define TIME_STEP 64

constexpr double maxMotorSpeed = 6.28;  // rad/s
constexpr double wheel_radius = 0.0205;  // m
constexpr int num_distance_sensors = 3;
constexpr double obstacleDistance = 90.0;

const std::array<std::string, num_distance_sensors> distanceSensorNames = { "dsL","dsF","dsR" };
const std::string MAP_FILE_NAME = "../../Map.txt";
const std::string PATH_PLAN_FILE_NAME = "../../MotionPlan.txt";
const std::string OUTPUT_FILE_NAME = "../../Output.txt";

// This is the main program of your controller.
// It creates an instance of your Robot instance, launches its
// function(s) and destroys it at the end of the execution.
// Note that only one instance of Robot should be created in
// a controller program.
// The arguments of the main function can be specified by the
// "controllerArgs" field of the Robot node

void addEdge(std::vector<int> adj[],int u, int v) { 
    adj[u].push_back(v);
    adj[v].push_back(u);
    auto it = std::unique(adj[u].begin(), adj[u].end());
    adj[u].resize(std::distance(adj[u].begin(), it));
    auto it2 = std::unique(adj[v].begin(), adj[v].end());
    adj[v].resize(std::distance(adj[v].begin(), it2));
    
    //std::cout << "size of u: " <<adj[u].size() <<" ,size of v: " << adj[v].size() << std::endl;
}



int getRow(int nV) {
    int row = 0;
    if (nV < 9) {
      row = 0;
    }
    else if (nV < 18) {
      row = 1;
    }
    else if (nV < 27) {
      row = 2;
    }
    else if (nV < 36) {
      row = 3;
    } else {
      row = 4;
    }
    
    return row;
}

int getCol(int nV) {
    int col = 0;
    
    col = nV % 9;
    
    
    return col;
}

std::pair<int, int> vertexToOutput(int nV)
{
  int y = getCol(nV) * 4 + 2;
  int x = getRow(nV) * 2;
  return std::make_pair(x, y);
}

bool checkStart(char input) {
  switch (input) {
    case '^':
        return true;
    case '>':
        return true;
    case 'v':
        return true;
    case '<':
        return true;
    default:
        return false;
  }

}


int getStartpos(char input) {
  switch (input) {
    case '^':
        return 0;
    case '>':
        return 1;
    case 'v':
        return 2;
    case '<':
        return 3;
    default:
        return -1;
  }
  

}

std::string getStartstring(int input) {
  switch (input) {
    case 0:
        return "N";
    case 1:
        return "E";
    case 2:
        return "S";
    case 3:
        return "W";
    default:
        return "FAILED TO GET STARTING DIRECTION PLEASE RESTART";
  }
  

}


int getDirection(int difference) {
   switch (difference) {
      case -9: //^
          return 0;
      case 1: //>
          return 1;
      case 9: //v
          return 2;
      case -1: // <
          return 3;
      default:
          return -1;
    }
  
}

std::string getPP(int curr_heading, int next_heading) {
    switch (curr_heading) {
        case 0:
            if (next_heading == 3) return "L";
            if (next_heading == 1) return "R";
            break;
        case 1:
            if (next_heading == 0) return "L";
            if (next_heading == 2) return "R";
            break;
        case 2:
            if (next_heading == 1) return "L";
            if (next_heading == 3) return "R";
            break;
        case 3:
            if (next_heading == 2) return "L";
            if (next_heading == 0) return "R";
            break;
    }
    return "LL";

}
 
/***************************************************************************************************
* The following function, which uses BFS to find all shortest paths, was adapted from:
* Title: find_paths source code
* Author: shobhitgupta907 (@shobhitgupta907), sanjeev2552
* Last Updated : 03 Feb, 2022
* Available at https://www.geeksforgeeks.org/print-all-shortest-paths-between-given-source-and-destination-in-an-undirected-graph/
***************************************************************************************************/

void find_paths(std::vector<std::vector<int> >& paths,
                std::vector<int>& path,
                std::vector<int> parent[],
                int n, int u)
{
    // Base Case
    if (u == -1) {
        paths.push_back(path);
        return;
    }
 
    // Loop for all the parents
    // of the given vertex
    for (int par : parent[u]) {
 
        // Insert the current
        // vertex in path
        path.push_back(u);
 
        // Recursive call for its parent
        find_paths(paths, path, parent,
                   n, par);
 
        // Remove the current vertex
        path.pop_back();
    }

}
 
// Function which performs bfs
// from the given source vertex
void bfs(std::vector<int> adj[],
         std::vector<int> parent[],
         int n, int start)
{
    // dist will contain shortest distance
    // from start to every other vertex
    std::vector<int> dist(n, INT_MAX);
 
    std::queue<int> q;
 
    // Insert source vertex in queue and make
    // its parent -1 and distance 0
    q.push(start);
    parent[start] = { -1 };
    dist[start] = 0;
 
    // Until Queue is empty
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : adj[u]) {
            if (dist[v] > dist[u] + 1) {
 
                // A shorter distance is found
                // So erase all the previous parents
                // and insert new parent u in parent[v]
                dist[v] = dist[u] + 1;
                q.push(v);
                parent[v].clear();
                parent[v].push_back(u);
            }
            else if (dist[v] == dist[u] + 1) {
 
                // Another candidate parent for
                // shortes path found
                parent[v].push_back(u);
            }
        }
    }
}
 
 

 
// Function which prints all the paths
// from start to end
void print_paths(std::vector<int> adj[], int n, int start, int end, std::string saveLine[], int startingPos){
    std::vector<std::vector<int> > paths;
    std::vector<int> path;
    std::vector<int> parent[n];
 
    // Function call to bfs
    bfs(adj, parent, n, start);
 
    // Function call to find_paths
    find_paths(paths, path, parent, n, end);
    int totalPaths = paths.size();
    //int pathLength = paths[0].size() - 2;
    int nV = 0;
    
    //std::cout << "[z5257127_MTRN4110_PhaseB] Finding shortest paths..." << std::endl;
    int nPaths = 1;
    int turns;
    int minTurn = INT_MAX;
    int dir = startingPos;
    int newDir = -1;
    int temp = start;
    int pathOfleastTurns = 0;
    std::string startCoords = std::to_string(getRow(start)) + std::to_string(getCol(start)) + getStartstring(startingPos);
    std::string pathPlan;
    std::vector<int>::iterator index;
    for (auto v : paths) {
 
        // Since paths contain each
        // path in reverse order,
        // so reverse it
        //reverse(v.begin(), v.end());
        nV = 0;

          turns = 0;
          temp = start;
          //reverse(v.begin(), v.end());
          dir = startingPos;
          for (int u : v) {
                if (u - temp != 0) {
                  newDir = getDirection((u - temp));
                  if (newDir != dir) {
                      if (abs(dir-newDir) == 1 ||abs(dir-newDir) == 3 ) {
                        turns++;
                      }
                      if (abs(dir-newDir) == 2) {
                        turns = turns + 2;
                      }
                      dir = newDir;
                  }
                  
                }
                temp = u;
         }

         if (turns < minTurn) {
           pathOfleastTurns = nPaths - 1;
           minTurn = turns;
         }
         reverse(v.begin(), v.end());

         //std::cout << "("<< getCol(u) << ","<< getRow(u) <<")" << " ";
       
        std::cout << std::endl;
        nPaths++;

    }

    nV = 0;
    auto v = paths[pathOfleastTurns];
    std::ofstream file_outputMap(OUTPUT_FILE_NAME,std::ios::trunc);

    std::cout << "[Robobot]  --- --- --- --- --- --- --- --- --- " << std::endl;
    file_outputMap << " --- --- --- --- --- --- --- --- --- " << "\n";
 /*         for(int j = 0; j < 9; j++) {
          std::cout << "[z5257127_MTRN4110_PhaseB] ";
            for(int c = 0; c < 37; c++) {
                if (c % 2 == 0 && c != 0 && c % 4 != 0 && j % 2 == 0 ) {
                    index = std::find(v.begin(), v.end(), nV);
                    if (nV != start &&  index != v.end() ) {
                      if (std::distance(v.begin(), index) > 9) {
                        c++;
                      }
                    } else {
                      std::cout << saveLine[j][c];

                    }
                    nV++;
                } else { 
                    std::cout << saveLine[j][c];  
                }
              }
              std::cout << std::endl;


           }*/
     for(int j = 0; j < 9; j++) {
          std::cout << "[Robobot] ";
            for(int c = 0; c < 37; c++) {
              std::cout << saveLine[j][c];
              file_outputMap <<  saveLine[j][c];
            }
            std::cout << std::endl;
            file_outputMap <<  "\n";
      }                    
    
    reverse(v.begin(), v.end());
    dir = startingPos;       
    for (auto ptr = v.begin(); ptr < v.end() - 1; ptr++){
        newDir = getDirection(*(ptr + 1) - *ptr);
        if (dir != newDir) {
          pathPlan = pathPlan + getPP(dir,newDir);
          dir = newDir;
        } 
        pathPlan = pathPlan + "F";
        
    }
    if (dir != 2) {
      pathPlan = pathPlan + getPP(dir,2);
    }
    std::cout << "[Robobot]  --- --- --- --- --- --- --- --- --- " << std::endl;
    file_outputMap << " --- --- --- --- --- --- --- --- --- " << "\n";
    file_outputMap.close();


   std::ofstream file(PATH_PLAN_FILE_NAME,std::ios::trunc);
    if (!file.is_open()) {
      std::cerr << "Cannot write to file";
    } else {
      file << startCoords << pathPlan;
      file.close();
    }
  

    //print lowest turn
    
    
    
}



//phase A



// Helper function to check for obstacles.


int mod(int a, int b) {
    return (a % b + b) % b;
}

auto executeMove(char command, double leftMotor, double rightMotor, char bearing, int row, int col) {
    //returns position for motors and updates rows, cols and heading
    int bearingINT;

    switch (bearing) {
    case 'N':
        bearingINT = 0;
        break;
    case 'E':
        bearingINT = 1;
        break;
    case 'S':
        bearingINT = 2;
        break;
    case 'W':
        bearingINT = 3;
        break;
    }
    //forward command
    if (command == 'F') {
        leftMotor = leftMotor + 2.62586 * M_PI;
        rightMotor = rightMotor + 2.62586 * M_PI;
        switch (bearing) {
        case 'N':
            row = row - 1;
            break;
        case 'E':
            col = col + 1;
            break;
        case 'S':
            row = row + 1;
            break;
        case 'W':
            col = col - 1;
            break;
        }

    }
    //left command
    else if (command == 'L') {
        leftMotor = leftMotor - 0.71117 * M_PI;
        rightMotor = rightMotor + 0.71117 * M_PI;
        bearingINT = mod((bearingINT - 1), 4);
    }
    //right command
    else if (command == 'R') {
        leftMotor = leftMotor + 0.71117 * M_PI;
        rightMotor = rightMotor - 0.71117 * M_PI;
        bearingINT = mod((bearingINT + 1), 4);
    }
    switch (bearingINT) {
    case 0:
        bearing = 'N';
        break;
    case 1:
        bearing = 'E';
        break;
    case 2:
        bearing = 'S';
        break;
    case 3:
        bearing = 'W';
        break;
    }
    struct motorPos { double leftMotor; double rightMotor; int row; int col; char bearing; };


    return motorPos{ leftMotor,rightMotor,row,col,bearing };

}

bool checkWall(double distanceValue) {
    if (distanceValue < 650) {
        return true;
    }
    else {
        return false;
    }
}

//auto deadRec(int row, int col, char heading, double diffR, double diffL, char command) {
    //transfer row col to cartesian
    //double x = col * 16.5;
  //  double y = -row * 16.5; //units in mm
            //
          //std::cout << "2: "<<currPoseR << std::endl;
         // diffR = currPoseR - prevPosR;
         // diffL = currPoseL - prevPosL;
         // std::cout <<"3: "<< diffR << std::endl;
         // changeS = ((0.020001509812471*diffL)/2) + ((0.020001509812471*diffR)/2);
        // changeZ = ((0.020001509812471*diffL)/0.056888894253924) + ((0.020001509812471*diffR)/0.056888894253924);

       //  x = x + changeS*cos(z+(changeZ/2));
         // y = y + changeS*sin(z+(changeZ/2));
         // z = z + changeZ;
          //z = normalize(z) * (M_PI/180);
          //


//
//}




int main(int argc, char **argv) {
    int n = 45;
    std::vector<int> adj[n];
    int src = 0;  //starting vertex
    int dest = 0; // destination = starting vertex
    int nV = 0;
    std::vector<int> notVisited = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44};
    std::vector<int> toVisit = {};
    std::cout << "[Robobot] --- --- --- --- --- --- --- --- --- " << std::endl;
    int col = 0;
    int row = 0;
    std::string saveLine[9];
    std::string Map;
    std::ifstream file(MAP_FILE_NAME);
    std::ofstream file2(OUTPUT_FILE_NAME,std::ios::trunc);
    
    if (file.is_open()) {
      if (!file2.is_open()) {
        std::cerr << "Cannot write to file";
      } 
      //std::cout << "[z5257127_MTRN4110_PhaseB] Reading in map from "<< MAP_FILE_NAME << "..."<<std::endl;
      while (std::getline(file, Map)) {
        //::cout << nV << "  "<< nV_2 <<std::endl;

      // Output the text from the file
        std::cout << "[Robobot] " << Map << std::endl;
        file2  << Map << "\n";
        if (row != 0 && row != 10){
            saveLine[row-1] = Map;
        }
        row++;
      }
      //std::cout << "[z5257127_MTRN4110_PhaseB] Map read in!"<<std::endl;
      file2 << "\n";
      file.close();
      file2.close();
    } else {
      std::cerr << "Cannot read file";
    }

    std::cout << "[Robobot] --- --- --- --- --- --- --- --- --- " << std::endl;
    
    //main map
    webots::Robot robot;
    // Get pointers to our robot's motors.
    std::unique_ptr<webots::Motor> leftMotor{ robot.getMotor("left wheel motor") };
    std::unique_ptr<webots::Motor> rightMotor{ robot.getMotor("right wheel motor") };
    leftMotor->setVelocity(0.0);
    rightMotor->setVelocity(0.0);
    leftMotor->setPosition(INFINITY);
    rightMotor->setPosition(INFINITY);
    //from workshop code
    std::array<std::unique_ptr<webots::DistanceSensor>, num_distance_sensors> distanceSensors;
    for (int i = 0; i < num_distance_sensors; i++) {
        distanceSensors[i] = std::make_unique<webots::DistanceSensor>(*robot.getDistanceSensor(distanceSensorNames[i]));
        distanceSensors[i]->enable(TIME_STEP);
    }
    int numMoves;
    int step;
    char heading;
    int moveCounter;
    double currTime;
    double prevTime;
    double leftPos = 0;
    double rightPos = 0;
    int aveLeft;
    int aveRight; 
    int aveFront;
    int aveTop;
    int sum;
    //main loop while notVisited not empty
    while (!notVisited.empty()) {
     aveLeft = 0;
     aveRight = 0; 
     aveFront = 0;
     aveTop = 0;
      print_paths(adj, n, src, dest,saveLine,2);
      std::string moveCommands;
      std::ifstream file("../../MotionPlan.txt");
      //std::cout << "[z5257127_MTRN4110_PhaseA] Reading in motion plan from ../../MotionPlan.txt..." << std::endl;
  
      if (file.is_open()) {
          while (std::getline(file, moveCommands)) {
              // Output the text from the file
              //std::cout << "[z5257127_MTRN4110_PhaseA] Motion Plan: " << moveCommands << std::endl;
          }
          file.close();
      }
      else {
          std::cerr << "Cannot read file";
      }
 

    //std::cout << "[z5257127_MTRN4110_PhaseA] Motion plan read in!" << std::endl;
    //Initial data from move file
     numMoves = moveCommands.length();
     step = 0;
     row = moveCommands[0] - '0';
     col = moveCommands[1] - '0';
     heading = moveCommands[2];
     moveCounter = 3;
     currTime = 0;
     prevTime = 0;
     sum = 0;
     //std::cout << "[z5257127_MTRN4110_PhaseA] Executing motion plan..." << std::endl;
    while (1) {
        //std::cout << robot.getTime() << std::endl;
        //Get average values for distance sensors

        if (moveCounter < numMoves) {

            auto motorPos = executeMove(moveCommands[moveCounter], leftPos, rightPos, heading, row, col);
            leftMotor->setVelocity(0.15 * maxMotorSpeed);
            rightMotor->setVelocity(0.15 * maxMotorSpeed);

            leftMotor->setPosition(motorPos.leftMotor);
            rightMotor->setPosition(motorPos.rightMotor);
            prevTime = robot.getTime();
            robot.step(1);
            while (robot.getTime() < prevTime + 9) {
                robot.step(1);
                //std::cout << "waiting" << std::endl;
            }
            leftPos = motorPos.leftMotor;
            rightPos = motorPos.rightMotor;
            row = motorPos.row;
            col = motorPos.col;
            heading = motorPos.bearing;
            step++;
            moveCounter++;

        }
        else {
                currTime = robot.getTime();
                robot.step(1);
                while(robot.getTime() < currTime + 3) {
                    robot.step(1);
                    aveLeft = distanceSensors[0]->getValue() + aveLeft;
                    aveFront = distanceSensors[1]->getValue() + aveFront;
                    aveRight = distanceSensors[2]->getValue() + aveRight;
                    sum++;
                }
                aveLeft = aveLeft/sum;
                aveFront = aveFront/sum;
                aveRight = aveRight/sum;
            
            break;     
        }
    }
    //std::cout << "[RoboBot] Motion plan executed!" << std::endl;
    std::pair<int, int> src_toString = vertexToOutput(src);
    std::pair<int, int> dest_toString = vertexToOutput(dest);
    saveLine[src_toString.first][src_toString.second] = ' ';
   // std::cout << src_toString.first <<", "<< src_toString.second << std::endl;
    saveLine[dest_toString.first][dest_toString.second] = 'v';
    //std::cout << dest_toString.first <<", "<< dest_toString.second << std::endl;
    std::vector<int>::iterator it;
  
    if (checkWall(aveFront) && getRow(dest) != 4) {
      saveLine[dest_toString.first + 1][dest_toString.second - 1] = '-';
      saveLine[dest_toString.first + 1][dest_toString.second] = '-';
      saveLine[dest_toString.first + 1][dest_toString.second + 1] = '-';
    } 
    if (!checkWall(aveFront) && getRow(dest) != 4) {
        it = std::find(notVisited.begin(), notVisited.end(), dest + 9);
        if (it != notVisited.end()) {
          toVisit.push_back(dest + 9);
        }
          addEdge(adj,dest,dest + 9);
        
    } 
    if (checkWall(aveLeft) && getCol(dest) != 8) {
      saveLine[dest_toString.first][dest_toString.second + 2] = '|';
      
    } 
    if (!checkWall(aveLeft) && getCol(dest) != 8) {
        it = std::find(notVisited.begin(), notVisited.end(), dest + 1);
        if (it != notVisited.end()) {
          toVisit.push_back(dest + 1);
        }
        addEdge(adj,dest,dest + 1);

    } 
    
    if (checkWall(aveRight) && getCol(dest) != 0) {
      saveLine[dest_toString.first][dest_toString.second - 2] = '|';
      
    } 
    if (!checkWall(aveRight) && getCol(dest) != 0) {
        it = std::find(notVisited.begin(), notVisited.end(), dest - 1);
        if (it != notVisited.end()) {
          toVisit.push_back(dest - 1);
        }
        addEdge(adj,dest,dest - 1);

    } 
    //rotate again to face -> to get top 
    auto motorPos = executeMove('L', leftPos, rightPos, heading, row, col);
    leftMotor->setVelocity(0.15 * maxMotorSpeed);
    rightMotor->setVelocity(0.15 * maxMotorSpeed);
    leftMotor->setPosition(motorPos.leftMotor);
    rightMotor->setPosition(motorPos.rightMotor);
    prevTime = robot.getTime();
    robot.step(1);
    while (robot.getTime() < prevTime + 9) {
        robot.step(1);
        //std::cout << "waiting" << std::endl;
    }
    leftPos = motorPos.leftMotor;
    rightPos = motorPos.rightMotor;
    row = motorPos.row;
    col = motorPos.col;
    heading = motorPos.bearing;
    currTime = robot.getTime();
    robot.step(1);
    sum = 0;
    
    while(robot.getTime() < currTime + 3) {
        robot.step(1);
        aveTop = distanceSensors[0]->getValue() + aveTop;
        sum++;
    }
    aveTop = aveTop/sum;
    if (checkWall(aveTop) && getRow(dest) != 0) {
      saveLine[dest_toString.first - 1][dest_toString.second - 1] = '-';
      saveLine[dest_toString.first - 1][dest_toString.second] = '-';
      saveLine[dest_toString.first - 1][dest_toString.second + 1] = '-';
    } 
    if (!checkWall(aveTop) && getRow(dest) != 0) {
        it = std::find(notVisited.begin(), notVisited.end(), dest - 9);
        if (it != notVisited.end()) {
          toVisit.push_back(dest - 9);
        }
          addEdge(adj,dest,dest - 9);
    } 
 
    motorPos = executeMove('R', leftPos, rightPos, heading, row, col);
    leftMotor->setVelocity(0.15 * maxMotorSpeed);
    rightMotor->setVelocity(0.15 * maxMotorSpeed);
    leftMotor->setPosition(motorPos.leftMotor);
    rightMotor->setPosition(motorPos.rightMotor);
    prevTime = robot.getTime();
    robot.step(1);
    while (robot.getTime() < prevTime + 9) {
        robot.step(1);
        //std::cout << "waiting" << std::endl;
    }
    leftPos = motorPos.leftMotor;
    rightPos = motorPos.rightMotor;
    row = motorPos.row;
    col = motorPos.col;
    heading = motorPos.bearing;
    currTime = robot.getTime();
    //new src and dest
    src = dest;
    //remove from notVisite
    
    auto it2 = std::unique(toVisit.begin(), toVisit.end());
    toVisit.resize(std::distance(toVisit.begin(), it2));
    std::remove(notVisited.begin(), notVisited.end(), dest);

    if (toVisit.size() == 0) {
      exit(0);
    }
    dest = toVisit.back();
    
   

   // std::cout << "3.." << toVisit.front() << std::endl;
    toVisit.pop_back();

  
    }
  return 0;
}
