% Project 2 Main file.
% Use this file to call your project2 function from the project2 file.
% Feel free to modify it as you see fit!

% Declare number of parcels = 3
totalNumberOfParcels = 3;

% Change pauseTime. Currently set to 0.5
pauseTime = 0.5;

% Desired positions for the parcels
desiredParcels = [
[0 0 0 0 0 0];
[0 0 0 0 0 0];
[0 0 0 0 0 0];
[1 2 3 0 0 0];
];


% Now lets call our algorithm passing in the arguments that we have
% declared above.
sim = project2(desiredParcels,totalNumberOfParcels,pauseTime);

% Get out final positions
finalPositions = sim.positions();


% Now lets display our final positions
disp("The final positions of all of the parcels are:")
disp(finalPositions);
delete(sim);