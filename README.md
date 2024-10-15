# University Projects
Here lies some of the projects I have worked on during my time in University

### project-backend-master
Source code for SoftEng Fundamentals course for flask backend development in python. This was a group project and my contributions include:
- Writing blackbox tests for authentication functions, handle generation function, Adminstration functions
- Writing most of the HTTP testing for all other functions
- Developing the authentication functionality including handle generation, adminstration functions, generating tokens and session ids, hashing data, unwrapping tokens,
- Helped with a majority of bug fixes and pylint/coverage issues

### snake
Source code for a mips project for Comp systems fundamentals, simulates the classice snake game using mips.

### ugv-code
Source code for a mechatronics project to develop a complete software package to control the Unmanned Ground Vehicle (UGV) using C++ with .NET frameworks. Modules included:
- Authentication for remote connection
- Laser
- GNSS
- Motion Control
- Camera
Additionally, created visual representation using opengl, of the lidar as well as display location and heading of the robot and its gps location.

### Autonomous Systems
Solution to problems in Autonomous Systems simulated data in Matlab
P1 implementing data processing and extraction for simulated data of a UGV:
-  Adds deckreckoning function
-  Process LiDar scan
-  Estimation of positions of Objects of interests
P2 Continues of p2:
- Adds EKF localization
- Adds estimation of ugv pose and gyroscope bias

### Thesis
For my group project thesis, We had to develop a weight measuring system within a dialysis chair. For my part I :
- Create and designed the code that runs on the arduino
- Made a rudimentary prototype to test software on, made from an arduino nano, SparkFun Qwiic Scale, load cell, Liquid crystal display and some scrap electronics and parts for the load cell base.
![prototype image](https://github.com/steve-ly/Uni-Projects/blob/main/thesis-part/prototype.jpg)
- Helped with assimalating the electrical components and software for the final design
- Troubleshooting and testing of the final product
![Final design image](https://github.com/steve-ly/Uni-Projects/blob/main/thesis-part/final.jpg)

### Robot Design
For this project, it was divided into 4 separate parts, ABC were down by me individually while D was a group project where we had to decide whose parts we would use to combine into 1
singular code base. While all 3 parts used were mine, I did not contribute to the refactoring and combination. Additionally, D also included extra functionality. This project comprised of python,
c++ and webots and was a simulation on the micromouse competitions.
* Part A - Locomotion:
On webots using C++, the robot had to be able to read in a file with commands that determine the robots movement. It should also display the initial heading as well as the heading as it steps through the instructed commands.
Additionally, using the unit sensor on the robot, determine whether there is a wall in front, to the left or right of the robot. This information would then be outputted to a csv file.
* Part B - Path Planning:
In c++, a file of the map of the robot is to be read and using Breadth first search, determine the shortest path. The code required that:
  - All shortest paths from one vertex to an other should be printed and showing a numbered steps of the robots traversal
  - It should find the shortest path with the least amount of turns then generate the movement sequence in the same format as the commands in Part A.
* Part C - Computer Vision:
In python using Juypter Notebook and opencv, Read in a picture of the map that the robot may be required to operate in. It should display the path in the same format as the map in part B. The code uses open cv to determine
the corners of the map in order to do a perspective transform so that the image is always a rectangle. The code also detects the qr image on the robot to determine its initial heading and pose. The true target is marked with an image
of a ladybug while the false target is marked with something similar. The code should also mark the true target while ignoring the false one. After detecting the walls, robot locationa and heading, true target, it outputs a map in the format found
in Part B.
* Part D - Integration:
Combining all 3 parts of the code and developed more cababilities for the robot. The additional tasks I completed for the robot includes:
  - Motion tracking the robot using opencv as well as determining its coordinates
  - Exploration module which uses BFS algorithm to allow the robot to automatically map out the maze.
  - Obstacle avoidance module, which would use BFS to reroute the robot when its senses an object on the path.
  
### palletizing
This project required scripting in matlab to control the URE 5 robot arm for a palletising task based on the tower of hanoi problem.
The robot would use a vacuum gripper attachment to lift up planks of wood of varying size. For a video demo you can find it here: [video link](https://drive.google.com/file/d/1-_TWV_ma9WwfPEhG4WtLi8QQHOPGrq6E/view?usp=drive_link)

### front end
PartA: Created a vanilla js frontend project for a job board website
PartB: Created a React js frontend project with bootstrap for a quiz website

### Unreal Engine 5 project
For computer graphics course, I had created a small game in unreal engine 5.
This project required a lot of assets, some borrowed and customized whilst others I had made myself. The gameplay and interaction was done through the blueprint system. Additionally I also implemented a very basic Ai enemy
within one of the difficulties as well as rigged the animations for it. 
It is currently on a google drive due to its size:
[Source code](https://drive.google.com/file/d/19JvxRDfNRCIZtBkcLZK71vVI5cYyGhNR/view?usp=drive_link)
[Packaged Game](https://drive.google.com/file/d/10QhxezOSdgthsDnMqt3IjPpdvVIS4dv7/view?usp=drive_link)
