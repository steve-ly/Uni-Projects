%Driver code by Jose guivant
%Implementation of part C by Steven Ly z5257127

%Example, showing how to read the data which is used in some problems in
%Tutorial2.problem 4, and in Project1/parts A,B,C.
%MTRN4010.T1.2022


% ---------------------------------------------------------------------------------
% ---------------------------------------------------------------------------------
function Solution_C(filename)
%filename is string
% load data, to be played back.
load(filename); % will load a variable named data (it is a structure) 
bias_guess = double(input('Enter intial bias guess as deg/s: ')) *pi/180;
cost = @(bias) ExploreDataGetCost(bias,data);
bias_est = fminsearch(cost,bias_guess);
disp('Bias = ');
disp([num2str(bias_est*180/pi),' deg/s']);
end


function cost = ExploreDataGetCost(bias,data)
Xe=data.pose0;   %platform's initial pose; [x0;y0;heading0]   [meters;meters;radians]
% it is necessary,for out task.

% I "copy" variables, for easy access (btw: Matlab copies vars "by reference", if used for reading)
                  % how many events?
table=data.table;           % table of events.
event = table(:,1);         % first event.

t0=event(1) ; t0=0.0001*double(t0); % initial time.


vw=[0;0];  % To keep last [speed,heading rate] measurement.
cost = 0;
[~,ncols] = size(table);
% t_final = 0.0001*double(table(1,ncols-1));
% t = t_final-40;  
t = t0;
t_final = t0 + 35;
% info: 'LiDAR's pose in UGV's CF=[Lx;Ly;Alpha], in [m,m,°]'
% It needs to be considered in your calculations.
%................

% Loop: read entries, one by one, for sequential processing.
GT = data.verify.poseL;
i = 0;
while t<t_final & i < ncols,
    i = i+1;
    
    event = table(:,i);
    sensorID=event(3);                         % source (i.e. which sensor?)
    t=0.0001*double(event(1));                  % when was that measurement taken?
    dt=t-t0;t0=t;                               % dt since last event (needed for predictions steps).
    % perform prediction X(t+dt) = f(X,vw,dt) ; vw model's inputs (speed and gyroZ) 
        
    
    here = event(2);                            % where to read it, from that sensor recorder.
    Xe = Deadreck(Xe,vw,dt);
    switch sensorID    %measurement is from?
        
        case 1  %  it is a scan from  LiDAR#1!
        %fprintf('LiDAR scan at t=[%d],dt=[%d]\n',t,dt); 
        Xgt = GT(:,here);
        
        cost = cost + pdist([Xgt(1,1),Xgt(2,1);Xe(1,1),Xe(2,1)],'euclidean');
       
        continue;  %"next!"
        
        %...............................
        case 2  %  it is speed encoder + gyro  (they are packed together)
        vw=data.vw(:,here);    % speed and gyroZ, last updated copy.
        vw(2) = vw(2)-bias;       
        continue;  %"next!"
        
        otherwise  % It may happen if the dataset contains measurements from sensors 
                     %which you had not expected to process.
        %fprintf('unknown sensor, type[%d], at t=[%d]\n',sensorID, t);         
        continue;
    end;
end;    

end
% --------------------------------------------------------------------------------

function Xe = Deadreck(Xe,vw,dt)
    h = Xe(3);
    dpose = [vw(1)*cos(h); vw(1)*sin(h); vw(2)];
    Xe = Xe + dt*dpose;

end



