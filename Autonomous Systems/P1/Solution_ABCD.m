%Driver code by Jose guivant
%Implementation of part ABCD by Steven Ly z5257127

%Example, showing how to read the data which is used in some problems in
%Tutorial2.problem 4, and in Project1/parts A,B,C.
%MTRN4010.T1.2022

% if you have questions, ask the lecturer, via Moodle or email(
% j.guivant@unsw.edu.au)

% ---------------------------------------------------------------------------------
function Solution_ABCD(filename)
%filename is string
% load data, to be played back.
load(filename); % will load a variable named data (it is a structure)  
ExploreData(data);
end

function ExploreData(data)
% Here, sensors' measurements are ordered by timestamp.
% as they had occurred, chronologically, when the data was collected/generated
% (in a real experiment o in simulation).
% Each line of this table contains an entry which describes a particular event (e.g. a measurement):
% --> The sampling time of the measurement, the sensor type, and an index to a record in the list of the recorded measurements of that
% particular sensor. So, we use that index to read to the specific measurement.

%Y you may initialize your program, before iterating through the list of events.
hh=InitCertainPartOfMyProgram(data);
figure(11); hold on;

ph = [plot(0, 0, '*b');  % for the platform
      plot(0, 0, '.m');  % for the LiDAR points
      plot(0, 0, '-b'); %plot ugv simulated heading
      plot(0,0, '+k'); %plot landmarks
      plot(0, 0, '-c'); %partA simulated pose
      plot(0,0,'*y');
      ]; 

X=data.pose0;   %platform's initial pose; [x0;y0;heading0]   [meters;meters;radians]
% it is necessary,for out task.

% I "copy" variables, for easy access (btw: Matlab copies vars "by reference", if used for reading)
ne=data.n;                   % how many events?
table=data.table;           % table of events.
event = table(:,1);         % first event.

t0=event(1) ; t0=0.0001*double(t0); % initial time.


vw=[0;0];  % To keep last [speed,heading rate] measurement.
XX=zeros(3,ne,'single');     % a buffer for my results.  size=3xne.
%................
etc=data.LidarCfg;  %Info about LiDAR installation (position and orientation, ..
% .. in platform's coordinate frame.). 

% info: 'LiDAR's pose in UGV's CF=[Lx;Ly;Alpha], in [m,m,°]'
% It needs to be considered in your calculations.
%................

% Loop: read entries, one by one, for sequential processing.
Landmarks=data.Landmarks;
Walls = data.Walls;

estPos = [];
estposition = [X(1,1),X(2,1),X(3,1)]; %init estposition as initial pose
for i=1:ne,
    
    XX(:,i)=X;
    
    event = table(:,i);
    sensorID=event(3);                         % source (i.e. which sensor?)
    t=0.0001*double(event(1));                  % when was that measurement taken?
    dt=t-t0;t0=t;                               % dt since last event (needed for predictions steps).
    % perform prediction X(t+dt) = f(X,vw,dt) ; vw model's inputs (speed and gyroZ) 
    X = get_pose(X,vw,dt); %part A
    plot_ugv(ph,X);%simulate ugv
    
    
    here = event(2);                            % where to read it, from that sensor recorder.
        
    switch sensorID    %measurement is from?
        
        case 1  %  it is a scan from  LiDAR#1!
        %fprintf('LiDAR scan at t=[%d],dt=[%d]\n',t,dt); 
        ranges = data.scans(:,here);  
        tic;
        [pp, ooi] = processLiDAR(ranges);  % e.g. for showing scan in "global CF", etc.
        toc


        %simulation for local cf lidar scans with ooi 
        figure(2);
        title('Local CF from Lidar');
        plot(pp(1,:),pp(2,:),'r.'); axis equal;       
        hold on;
        plot(ooi(1,:),ooi(2,:),'+k');
        hold off;

        pause(dt/4);

        [landmarks_for_tri,ooi_local] = data_assoc(pp,ph,X,etc,ooi,Landmarks); %data association
        estposition = Trilateration(landmarks_for_tri,ooi_local,estposition);
        position = [estposition(1,1);estposition(1,2)];
        estPos = [estPos position];
        continue;  %"next!"
        
        %...............................
        case 2  %  it is speed encoder + gyro  (they are packed together)
        vw=data.vw(:,here);    % speed and gyroZ, last updated copy.
       
        fprintf('new measurement: v=[%.2f]m/s,w=[%.2f]deg/sec\n',vw.*[1;180/pi]);
        continue;  %"next!"
        
        otherwise  % It may happen if the dataset contains measurements from sensors 
                     %which you had not expected to process.
        %fprintf('unknown sensor, type[%d], at t=[%d]\n',sensorID, t); 
        
            
        continue;
        
    end;    
end;    


%plot calculated pose vs real pose vs localization estimation
figure(11)
hold on;
plot(estPos(1,:),estPos(2,:),'k.');
plot(XX(1,:),XX(2,:),'g.');





disp('Loop of events ends.');
disp('Showing ground truth (you would not achieve that, exactly.)');
ShowVerification1(data);
end
% --------------------------------------------------------------------------------

function hh=InitCertainPartOfMyProgram(data)
    % you may initialize things you need.
    % E.g.: context for some dynamic plots,etc.
    
    % for local CF.
    
    %figure(10); clf();       % create a figure, or clear it if it does exist.
    %r0=zeros(321,1);         % dummy lidar scan.
    %h1=plot(r0,'.');          % h: handle to this graphic object, for subsequent use.  
    %axis([1,321,0,15]);  % my region of interest, to show.
    %hold on;     plot([1,321],[10,10],'--r');  % just some line.
    %zoom on;     % by default, allow zooming in/out
    %title('LiDAR scans (polar)(removed from this demo)');  
    %ylabel('ranges (m)');
    

    % for global CF.
    
figure(11); clf();    % global CF.

% show the map landmarks and, if it is of interest to verify your solution, the
% walls/infrastructure present there.
% (All of them are provided in Global CF)

Landmarks=data.Landmarks;
% plot centres of landmarks. 
%plot(Landmarks(1,:),Landmarks(2,:),'+');
%hold on;
plot(Landmarks(1,:),Landmarks(2,:),'o' ,'color',0*[0,1/3,0])
% some pixels will appear close to some of these crosses. It means he LiDAR scan is
% detecting the associated poles (5cm radius).


% plot interior of walls (they have ~20cm thickness; but the provided info just includes the ideal center of the walls
% your LiDAR scans will appear at ~ 10cm from some of those lines.    
% Wall transversal section:  :  wall left side [<--10cm-->|<--10cm-->] the other  wall side. 
hold on;
plot(data.Walls(1,:),data.Walls(2,:),'color',[0,1,0]*0.7,'linewidth',3);
%legend({'Centers of landmarks','Walls (middle planes) '});

title('Global CF (you should show some results here)');
xlabel('X (m)'); 
ylabel('Y (m)');
p0=data.pose0;
plot(p0(1),p0(2),'bs');
%legend({'Landmarks','Walls (middle planes)','initial pose'});




hh=[];  % array of handles you may want to use in other parts of the program.
% empty now.
end

function ShowVerification1(data)

% plot some provided verification points (of platfom's pose).
% those are the ground truth.
% Do not expect your solution path to intesect those points, as those are
% the real positions, and yours are approximate ones, based on
% predictions, and using sampled inputs. 
% The discrepancy should be just fraction of cm, as the inputs are not
% polluted by noise, and the simulated model is the nominal analog model.
% The errors are mostly due to time discretization and sampled inputs.
% Inputs were sampled @100Hz (10ms) (you can infer that from "dt".
figure(11)
hold on;
p=data.verify.poseL;
plot(p(1,:),p(2,:),'y.');
h=legend({'Landmarks','Walls (middle planes)','Initial pose','Ground truth (subsampled)','','','','','Real path','Estimate from part D','Predicted from part A'});
end


% ---------------------------------------------------------------------------------
function pose_new = get_pose(curr_pose,vw,dt) %part A
    h = curr_pose(3);
    dpose = [vw(1)*cos(h); vw(1)*sin(h); vw(2)];
    pose_new = curr_pose + dt*dpose;

end

function plot_ugv(ph, pose)
    set(ph(1), 'xdata', pose(1), 'ydata', pose(2));
    heading = [pose(1), 3*cos(pose(3))+pose(1); pose(2), 3*sin(pose(3))+pose(2)];
    set(ph(3), 'xdata', heading(1, :), 'ydata', heading(2, :));
end



function [pp,ooi] = processLiDAR(ranges) %part b
% process LiDAR scan.
% your implementation.    
% You decide the input and ouput variables, etc.
% showing the LiDAR in local CF, was shown in the tutorial explanation. You
% may copy that from there to here.
% I am not refreshing scans now, so you do not need to wait for the
% animation to end. This example source code has other purposes.
    rr = single(ranges)*0.01; % cm to m
    aa = deg2rad(-80:0.5:80); % 321 points
    ii = find((rr > 1) & (rr < 20));
    rr = rr(ii)';
    aa = aa(ii);
    
    xx = rr.*cos(aa);
    yy = rr.*sin(aa);
    pp = [xx; yy];
    copy = pp;
    [~,ncols] = size(copy);
    ooi = zeros(2,1);
     found_start = 0;
     %for i = 1:ncols-2
      %  meas1 = [copy(1,i),copy(2,i);copy(1,i+1),copy(2,i+1)];
       % meas2 = [copy(1,i+1),copy(2,i+1);copy(1,i+2),copy(2,i+2)];
       % if abs(pdist(meas1) - pdist(meas2)) > 0.3 & found_start == 0
        %    start = i+2;
         %   found_start = 1;
         %   i = start;
        %elseif abs(pdist(meas1) - pdist(meas2)) > 0.3 & found_start == 1
         %   A = copy(1:2,start:i+1);
          %  centre = mean(A,2);
           % ooi = [ooi centre];
            %found_start = 0;      
        %end
     %end
     for i = 1:ncols-2
       meas1 = [copy(1,i),copy(2,i);copy(1,i+1),copy(2,i+1)];
        meas2 = [copy(1,i+1),copy(2,i+1);copy(1,i+2),copy(2,i+2)];
        if abs(pdist(meas1,'euclidean') - pdist(meas2,'euclidean')) > 0.15 & found_start == 1 
            A = copy(1:2,start:i+1);
            [~,ooi_detected] = size(A);
            if ooi_detected < 8
            centre = mean(A,2);
            ooi = [ooi centre];
            end
            found_start = 0;
        
        elseif abs(pdist(meas1,'euclidean') - pdist(meas2,'euclidean')) > 0.15 & found_start == 0
            start = i+2;
            found_start = 1;
            i = start;
            
        elseif pdist(meas1,'euclidean') > 0.15 & pdist(meas2,'euclidean') > 0.15 %single point
            centre = [copy(1,i+1);copy(2,i+1)];
            ooi = [ooi centre];
        end
     end
    % this is to avoid Matlab trying to interprete LaTex (our filenames have
    % character '_')
    % 


    
    
    


    % shown in local CF.
% You may introduce a delay (using pause(...) ), here; if we are showing some dynamic plots.









end


function [landmarks_for_tri,ooi_local] = data_assoc(pp,ph,X,etc,ooi,Landmarks) %part C
    landmarks_for_tri = [];
    ooi_local = [];
    ooi_local_Cog = ooi;
    %move to ugv pov
    h1  = etc.Alpha * pi/180;
    R  = [[cos(h1), -sin(h1)]; [sin(h1), cos(h1)]];
    pp = R * pp;
    pp(1, :) = pp(1, :) + etc.Lx;
    pp(2, :) = pp(2, :) + etc.Ly;
    
    ooi = R * ooi;
    ooi(1, :) = ooi(1, :) + etc.Lx;
    ooi(2, :) = ooi(2, :) + etc.Ly;
    %move to global
    h  = X(3);
    R  = [[cos(h), -sin(h)]; [sin(h), cos(h)]];
    pp = R * pp;
    pp(1, :) = pp(1, :) + X(1);
    pp(2, :) = pp(2, :) + X(2);
    
    ooi = R * ooi;
    ooi(1, :) = ooi(1, :) + X(1);
    ooi(2, :) = ooi(2, :) + X(2);
    
    %compare ooi to landmarks
    [~,ncols] = size(Landmarks);
    [~,ncols1] = size(ooi);
    %[~,ncols2] = size(Walls);

    poles_filter = zeros(2,1);
    %not_wall = 1;
    for i = 1:ncols
        for j = 1:ncols1
            meas = [Landmarks(1,i),Landmarks(2,i);ooi(1,j),ooi(2,j)];
            if pdist(meas,'euclidean') < 0.4    
                ispole = [ooi(1,j);ooi(2,j)];
                ispole_local = [ooi_local_Cog(1,j);ooi_local_Cog(2,j)];
                confirm_landmark = [Landmarks(1,i);Landmarks(2,i)];
                poles_filter = [poles_filter ispole];
                 %[landmarks_local ispole_inLocal];
                landmarks_for_tri = [landmarks_for_tri confirm_landmark];
                ooi_local = [ooi_local ispole_local];

            end
        end
    
    end
    
    


    
    set(ph(2), 'xdata', pp(1, :), 'ydata', pp(2, :));
    set(ph(4), 'xdata', poles_filter(1, :), 'ydata', poles_filter(2, :));

    
    
end

% 
% function estposition = Trilateration(landmarks_for_tri,ooi_local,prev_pose)
%         [~,ncols] = size(landmarks_for_tri);
%         z = prev_pose;
%         x0 = [double(prev_pose(1,1)),double(prev_pose(1,2))];
%         if ncols > 2
%             [~,range1] = cart2pol(ooi_local(1,1),ooi_local(2,1));
%             [~,range2] = cart2pol(ooi_local(1,2),ooi_local(2,2));
%             [~,range3] = cart2pol(ooi_local(1,3),ooi_local(2,3));
%             fun = @(x) [double(range1) - sqrt((x(1)-double(landmarks_for_tri(1,1)))^2 +(x(2)-double(landmarks_for_tri(2,1)))^2 );
%                 double(range2) - sqrt((x(1)-double(landmarks_for_tri(1,2)))^2 +(x(2)-double(landmarks_for_tri(2,2)))^2 ) ;
%                 double(range3) - sqrt((x(1)-double(landmarks_for_tri(1,3)))^2 +(x(2)-double(landmarks_for_tri(2,3)))^2 )
%             ];
%         z = fsolve(fun,x0);
%         end
%         estposition = z;
% 
% end

function estposition = Trilateration(landmarks_for_tri,ooi_local,prev_pose) %part D
        [~,ncols] = size(landmarks_for_tri);
        z = prev_pose;
        x0 = [double(prev_pose(1,1)),double(prev_pose(1,2)),double(prev_pose(1,3))];
        if ncols > 2
            [bearing1,range1] = cart2pol(ooi_local(1,1),ooi_local(2,1));
            [bearing2,range2] = cart2pol(ooi_local(1,2),ooi_local(2,2));
            fun = @(x) [double(range1) - sqrt((x(1)-double(landmarks_for_tri(1,1)))^2 +(x(2)-double(landmarks_for_tri(2,1)))^2 );
                double(range2) - sqrt((x(1)-double(landmarks_for_tri(1,2)))^2 +(x(2)-double(landmarks_for_tri(2,2)))^2 ) ;

                double(bearing1) - atan2(double(landmarks_for_tri(2,1))-x(2),double(landmarks_for_tri(1,1))-x(1)) + x(3);
                double(bearing2) - atan2(double(landmarks_for_tri(2,2))-x(2),double(landmarks_for_tri(1,2))-x(1)) + x(3);
                
                ];
            z = fsolve(fun,x0);
            x0 = z;
            for i = 3:ncols
            [bearing,range] = cart2pol(ooi_local(1,i),ooi_local(2,i));
            fun = @(x) [double(range) - sqrt((x(1)-double(landmarks_for_tri(1,i)))^2 +(x(2)-double(landmarks_for_tri(2,i)))^2 );
            double(bearing) - atan2(double(landmarks_for_tri(2,i))-x(2),double(landmarks_for_tri(1,i))-x(1)) + x(3)
            ];
            z = lsqnonlin(fun,x0); 
            end
        end
        
        estposition = z;

end



% if you have questions, ask the lecturer, via Moodle or email(
% j.guivant@unsw.edu.au)
% or ask the demonstrators.
