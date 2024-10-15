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
}

void removeEdge(std::vector<int> adj[], int u, int v)
{
    // Traversing through the first vector list
    // and removing the second element from it
    for (int i = 0; i < adj[u].size(); i++) {
        if (adj[u][i] == v) {
            adj[u].erase(adj[u].begin() + i);
            break;
        }
    }
 
    // Traversing through the second vector list
    // and removing the first element from it
    for (int i = 0; i < adj[v].size(); i++) {
        if (adj[v][i] == u) {
            adj[v].erase(adj[v].begin() + i);
            break;
        }
    }
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
    
    std::ofstream file2(OUTPUT_FILE_NAME,std::ios::app);
    if (!file2.is_open()) {
      std::cerr << "Cannot write to file";
    }
    std::cout << "[Robobot] Finding shortest paths..." << std::endl;
    file2 << "[Robobot] Finding shortest paths..." << "\n";
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
        // Print node for the current path
          std::cout << "[Robobot] Path - " << nPaths << ":" << std::endl;
          file2 << "[Robobot] Path - " << nPaths << ":" <<"\n";

          std::cout << "[Robobot]  --- --- --- --- --- --- --- --- --- " << std::endl;
          file2 << "[Robobot]  --- --- --- --- --- --- --- --- --- " << "\n";

          for(int j = 0; j < 9; j++) {
          std::cout << "[Robobot] ";
          file2 << "[Robobot] ";
            for(int c = 0; c < 37; c++) {
                if (c % 2 == 0 && c != 0 && c % 4 != 0 && j % 2 == 0 ) {
                    index = std::find(v.begin(), v.end(), nV);
                    if (nV != start &&  index != v.end() ) {
                      std::cout << std::distance(v.begin(), index);
                      file2 << std::distance(v.begin(), index);
                      if (std::distance(v.begin(), index) > 9) {
                        c++;
                      }
                    } else {
                      std::cout << saveLine[j][c];
                      file2 << saveLine[j][c];
                    }
                    nV++;
                } else { 
                    std::cout << saveLine[j][c];
                    file2 << saveLine[j][c];
                }
              }
              std::cout << std::endl;
              file2 << "\n";

           }
            
          std::cout << "[Robobot]  --- --- --- --- --- --- --- --- --- " << std::endl;
          file2 << "[Robobot]  --- --- --- --- --- --- --- --- --- " << "\n";
          turns = 0;
          temp = start;
          reverse(v.begin(), v.end());
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
    std::cout << "[Robobot] " << totalPaths << " shortest paths found!"<< std::endl;
    file2 << "[Robobot] " << totalPaths << " shortest paths found!"<< "\n";

    std::cout << "[Robobot] Finding shortest path with least turns..."<< std::endl;
    file2 << "[Robobot] Finding shortest path with least turns..."<< "\n";
    nV = 0;
    auto v = paths[pathOfleastTurns];
    std::cout << "[Robobot]  --- --- --- --- --- --- --- --- --- " << std::endl;
    file2 << "[Robobot]  --- --- --- --- --- --- --- --- --- " << "\n";

          for(int j = 0; j < 9; j++) {
          std::cout << "[Robobot] ";
          file2 << "[Robobot] ";
            for(int c = 0; c < 37; c++) {
                if (c % 2 == 0 && c != 0 && c % 4 != 0 && j % 2 == 0 ) {
                    index = std::find(v.begin(), v.end(), nV);
                    if (nV != start &&  index != v.end() ) {
                      std::cout << std::distance(v.begin(), index);
                      file2 << std::distance(v.begin(), index);
                      if (std::distance(v.begin(), index) > 9) {
                        c++;
                      }
                    } else {
                      std::cout << saveLine[j][c];
                      file2 << saveLine[j][c];

                    }
                    nV++;
                } else { 
                    std::cout << saveLine[j][c];  
                    file2 << saveLine[j][c];
                }
              }
              std::cout << std::endl;
              file2 << "\n";


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
    
    std::cout << "[Robobot]  --- --- --- --- --- --- --- --- --- " << std::endl;
    file2 << "[Robobot]  --- --- --- --- --- --- --- --- --- " << "\n";
    std::cout << "[Robobot] Shortest path with least turns found!"<< std::endl;
    file2 << "[Robobot] Shortest path with least turns found!"<< "\n";
    std::cout << "[Robobot] Path Plan ("<< pathPlan.length() <<" steps): " << startCoords << pathPlan <<std::endl;
    file2 << "[Robobot] Path Plan ("<< pathPlan.length() <<" steps): " << startCoords << pathPlan <<"\n";
    std::cout << "[Robobot] Writing path plan to "<<PATH_PLAN_FILE_NAME <<"..." << std::endl;
    file2 << "[Robobot] Writing path plan to "<<PATH_PLAN_FILE_NAME <<"..." << "\n";
    std::cout << "[Robobot] Path plan written to "<<PATH_PLAN_FILE_NAME <<"!"<< std::endl;
    file2 << "[Robobot] Path plan written to "<<PATH_PLAN_FILE_NAME <<"!"<< "\n";
    file2.close();

   std::ofstream file(PATH_PLAN_FILE_NAME,std::ios::trunc);
    if (!file.is_open()) {
      std::cerr << "Cannot write to file";
    } else {
      file << startCoords << pathPlan;
      file.close();
    }
  

    //print lowest turn
    
    
    
}


// Helper function to check for obstacles.


int mod(int a, int b) {
    return (a % b + b) % b;
}

auto executeMove(char command, double leftMotor, double rightMotor, char bearing, int row, int col) {
    //returns position for motors and updates rows, cols and heading
    int bearingINT = -1;

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
std::pair<int, int> vertexToOutput(int nV)
{
  int y = getCol(nV) * 4 + 2;
  int x = getRow(nV) * 2;
  return std::make_pair(x, y);
}


int getObstacleVertex(int row, int col, char heading) {
    int obstacle_location = (row * 9) + col;
    int bearingINT = -1;

    switch (heading) {
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
    
    switch (bearingINT) {
    case 0:
        obstacle_location = obstacle_location - 9;
        break;
    case 1:
        obstacle_location = obstacle_location + 1;
        break;
    case 2:
        obstacle_location = obstacle_location + 9;
        break;
    case 3:
        obstacle_location = obstacle_location - 1;
        break;
    }
    return obstacle_location;
    
}

int headingToint(char bearing) {
    int bearingINT = -1;
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
    return bearingINT;
}

bool wallInway(double frontSensor,char movecommand,int src,std::string saveLine[9],char heading) {
    std::pair<int, int> coords = vertexToOutput(src);
    switch (heading) {
    case 'N':
        coords.first = coords.first + 1;
        break;
    case 'E':
        coords.second = coords.second + 2;
        break;
    case 'S':
        coords.first = coords.first - 1;
        break;
    case 'W':
        coords.second = coords.second - 2;
        break;
    }
    if (frontSensor < 650 && movecommand == 'F') {
       if (saveLine[coords.first][coords.second] != ' ') {
         return false;
       }
       else {
       return true;
       }
       
    } 
    else {
      return false;
    }
    
}
int main(int argc, char **argv) {
    int n = 45;
    std::vector<int> adj[n];
    int src = 0;
    int dest = 22;
    
    int nV = 0;
    int nV_2 = 0;
    std::string Map;
    std::ifstream file(MAP_FILE_NAME);

    int row = 0;
    int startPos = -1;
    std::string saveLine[9];
 
    if (file.is_open()) {
      std::cout << "[Robobot] Reading in map from "<< MAP_FILE_NAME << "..."<<std::endl;
      while (std::getline(file, Map)) {
        //::cout << nV << "  "<< nV_2 <<std::endl;

      // Output the text from the file
        std::cout << "[Robobot] " << Map << std::endl;
        if (row != 0 && row != 10){
            saveLine[row-1] = Map;
        }
        if(row % 2 != 0) {
          //std::cout << row <<std::endl;
          for (std::size_t j = 0; j < Map.length(); j++) {
             if (j % 4 == 0 && j != 0) {
               if(Map[j] != '|') {
                 addEdge(adj,nV,nV + 1);

               }
               nV++;
               
             }
             if (checkStart(Map[j])) {
               src = nV;
               startPos = getStartpos(Map[j]);

             }
             if(Map[j] == 'x') {
               dest = nV;
             }
           }
        }
        else if (row != 0 && row != 10) {
         for (std::size_t c = 0; c < Map.length(); c++) {
           if (c % 2 == 0 && c != 0 && c % 4 != 0)  {
              if(Map[c] != '-') {
                addEdge(adj,nV_2,nV_2 + 9);
              }
              nV_2++;
           } 
         }
       
       }

        row++;
      }
      std::cout << "[Robobot] Map read in!"<<std::endl;
      file.close();
    } else {
      std::cerr << "Cannot read file";
    }
    
  

    // Function Call
    print_paths(adj, n, src, dest,saveLine,startPos);
     // Initialise robot.
    webots::Robot robot;
    // Get pointers to our robot's motors.
    std::unique_ptr<webots::Motor> leftMotor{robot.getMotor("left wheel motor")};
    std::unique_ptr<webots::Motor> rightMotor{robot.getMotor("right wheel motor")};
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

    std::string moveCommands;
    std::ifstream pathfile(PATH_PLAN_FILE_NAME);
    std::cout << "[Robobot] Reading in motion plan from ../../MotionPlan.txt..." << std::endl;
    if (pathfile.is_open()) {
      while (std::getline(pathfile, moveCommands)) {
      // Output the text from the file
        std::cout << "[Robobot] Motion Plan: " << moveCommands <<std::endl;
      }
      pathfile.close();
    } else {
      std::cerr << "Cannot read file";
    }
   
    
    //15.74311 for cells
    
    int dest_row = getRow(dest);
    int dest_col = getCol(dest);
    
     std::cout << "[Robobot] Motion plan read in!"<<std::endl;
    //Initial data from move file
    int numMoves = moveCommands.length();
    int step = 0;
     row = moveCommands[0] - '0';
    int col = moveCommands[1] - '0';
    char heading = moveCommands[2];
    int moveCounter = 3;
    double currTime = 0;
    double prevTime = 0;
    double leftPos = 0;
    double rightPos = 0;
    int aveLeft = 0;
    int aveRight = 0;
    int aveFront = 0;
    int sum = 0;
    int ob;
    int current_heading;
    while (robot.step(TIME_STEP) != -1) {
        //std::cout << robot.getTime() << std::endl;
        //Get average values for distance sensors
      if (row == dest_row && col == dest_col) {
          exit(0);
      }
       aveLeft = 0;
       aveRight = 0;
       aveFront = 0;
       sum = 0;

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
        
        if (wallInway(aveFront,moveCommands[moveCounter],src,saveLine,heading)) {
           ob = getObstacleVertex(row, col, heading);
           removeEdge(adj,src, ob); 
           current_heading = headingToint(heading);
           print_paths(adj, n, src, dest,saveLine,current_heading);
           std::ifstream pathfile(PATH_PLAN_FILE_NAME);
           if (pathfile.is_open()) {
            while (std::getline(pathfile, moveCommands)) {
            // Output the text from the file
              std::cout << "[Robobot] Obstacle detected, Rerouting... " <<std::endl;
            }
            pathfile.close();
          } else {
            std::cerr << "Cannot read file";
          }
            numMoves = moveCommands.length();
            step = 0;
            row = moveCommands[0] - '0';
            col = moveCommands[1] - '0';
            heading = moveCommands[2];
            moveCounter = 3;
            currTime = 0;
            prevTime = 0;
            aveLeft = 0;
            aveRight = 0;
            aveFront = 0;
  
        }
        //write to file
        if (moveCounter < numMoves) {
            auto motorPos = executeMove(moveCommands[moveCounter],leftPos,rightPos,heading,row,col);
            leftMotor->setVelocity(0.15*maxMotorSpeed);
            rightMotor->setVelocity(0.15*maxMotorSpeed);

            leftMotor->setPosition(motorPos.leftMotor);
            rightMotor->setPosition(motorPos.rightMotor);
            prevTime = robot.getTime();
            robot.step(1);
            while (robot.getTime() < prevTime + 11) {
                 robot.step(1); 
            }
            leftPos = motorPos.leftMotor;
            rightPos = motorPos.rightMotor;
            row = motorPos.row;
            col = motorPos.col;
            heading = motorPos.bearing;
            step++;
            moveCounter++;
            src = (row * 9) + col;
        }

    }
  
  return 0;
}
