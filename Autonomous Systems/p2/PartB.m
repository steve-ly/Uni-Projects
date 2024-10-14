%Driver code by Jose guivant
%Implementation of part B by Steven Ly z5257127

%Example, showing how to read the data which is used in some problems in
%Tutorial2.problem 4, and in Project1/parts A,B,C.
%MTRN4010.T1.2022

% if you have questions, ask the lecturer, via Moodle or email(
% j.guivant@unsw.edu.au)

% ---------------------------------------------------------------------------------
function Solution_B(filename)
%filename is string
% load data, to be played back.
load(filename); % will load a variable named data (it is a structure)
AA=API_project1_AAS();
ExploreData(data,AA);
end

function ExploreData(data,API)
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
      plot(0,0,'*w');
      ]; 

X_y=data.pose0;
X = [X_y(1);X_y(2);X_y(3);0];
p_k = [0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,(0.1*pi/180)^2];
% (0.5*pi/180)^2
% p_k(1,1) = 0.1^2;
% p_k(2,2) = 0.1^2;
% p_k(3,3) = (0.5*pi/180)^2;
%platform's initial pose; [x0;y0;heading0]   [meters;meters;radians]
% it is necessary,for out task.

% I "copy" variables, for easy access (btw: Matlab copies vars "by reference", if used for reading)
ne=data.n;                   % how many events?
table=data.table;           % table of events.
event = table(:,1);         % first event.

t0=event(1) ; t0=0.0001*double(t0); % initial time.


vw=[0;0];  % To keep last [speed,heading rate] measurement.
XX=zeros(4,ne,'single');     % a buffer for my results.  size=3xne.
%................
etc=data.LidarCfg;  %Info about LiDAR installation (position and orientation, ..
% .. in platform's coordinate frame.). 

% info: 'LiDAR's pose in UGV's CF=[Lx;Ly;Alpha], in [m,m,°]'
% It needs to be considered in your calculations.
%................

% Loop: read entries, one by one, for sequential processing.
Landmarks=data.Landmarks;
Walls = data.Walls;

tt = [];
for i=1:ne,
    
    XX(:,i)=X;
    event = table(:,i);
    sensorID=event(3);                         % source (i.e. which sensor?)
    t=0.0001*double(event(1));                  % when was that measurement taken?
    tt(i) = i;
    dt=t-t0;t0=t;
    
    % dt since last event (needed for predictions steps).
    % perform prediction X(t+dt) = f(X,vw,dt) ; vw model's inputs (speed and gyroZ) 
    [X,p_k] = get_pose(X,vw,dt,p_k); %part A
%     plot_ugv(ph,prior_bias)
    plot_ugv(ph,X);%simulate ugv

    
    here = event(2);                            % where to read it, from that sensor recorder.
        
    switch sensorID    %measurement is from?
        
        case 1  %  it is a scan from  LiDAR#1!
        %fprintf('LiDAR scan at t=[%d],dt=[%d]\n',t,dt); 
        ranges = data.scans(:,here);  
        [pp, ooi] = processLiDAR(ranges,API);  % e.g. for showing scan in "global CF", etc.
        
        [~,ncols] = size(ooi);
       
            %simulation for local cf lidar scans with ooi 
            figure(2);
            title('Local CF from Lidar');
            plot(pp(1,:),pp(2,:),'r.'); axis equal;
            
        if ncols > 0     
            hold on;
            plot(ooi(1,:),ooi(2,:),'+k');
            hold off;
        end
        
        if ncols > 0 
            [landmarks,ooi_local] = data_assoc(pp,ph,X,etc,ooi,Landmarks,API); %data association
        end
        
        [~,cols] = size(landmarks);
        if cols > 0
            for j = 1:cols
                [X,p_k]  = updatestep(p_k,X,[ooi_local(1,j);ooi_local(2,j)],[landmarks(1,j);landmarks(2,j)]);
            end 
        end

%         disp(X(4)*180/pi);
        continue;  %"next!"
        
        %...............................
        case 2  %  it is speed encoder + gyro  (they are packed together)
        vw=data.vw(:,here);    % speed and gyroZ, last updated copy.
%         vw(2) = vw(2)-X(4);
        %fprintf('new measurement: v=[%.2f]m/s,w=[%.2f]deg/sec\n',vw.*[1;180/pi]);
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
plot(XX(1,:),XX(2,:),'k.');
% plot(X_Bias(1,:),X_Bias(2,:),'k.');






disp('Loop of events ends.');
disp('Showing ground truth (you would not achieve that, exactly.)');
ShowVerification1(data);

figure(4)
plot(tt(1,:),XX(4,:)*180/pi);
title('Bias b over time sample');
xlabel('Time Sample');
ylabel('Bias in deg/s');
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
plot(p(1,:),p(2,:),'c.');
h=legend({'Landmarks','Walls (middle planes)','Initial pose','Ground truth (subsampled)','','','','','','Estimate from part A','Real path'});
end


% ---------------------------------------------------------------------------------
function [est_pos,p_cov] = get_pose(curr_pose,vw,dt,p_k) %part A
    %h = curr_pose(3);
    %dpose = [vw(1)*cos(h); vw(1)*sin(h); vw(2)];
    %pose_new = curr_pose + dt*dpose;
    
    %State Prediction
    dpose = [vw(1)*cos(curr_pose(3)); vw(1)*sin(curr_pose(3)); vw(2)-curr_pose(4);0];
    est_pos = curr_pose + dt*dpose;
    
    j_k = [1,0,-dt*vw(1)*sin(curr_pose(3)),0;0,1,dt*vw(1)*cos(curr_pose(3)),0;0,0,1,-dt;0,0,0,1];
    q_u = [(5/100)^2,0;0,(pi/180)^2];

    j_u = [dt*cos(curr_pose(3)),0;dt*sin(curr_pose(3)),0;0,dt;0,0];
%     q = [(dt*0.01)^2,0,0,0;0,(dt*0.01)^2,0,0;0,0,0,0;0,0,0,(dt*(pi/180)/600)^2];
%     q = [0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,(dt*(pi/180)/600)^2];

    p_cov = j_k*p_k*j_k' + j_u*q_u*j_u';


end


function [ekf_pose,ekf_var] = updatestep(p_k,est_pose,ooi_measured,landmark)
   %Residual Innovation
%    [alpha,range] = cart2pol(ooi_measured(1,1),ooi_measured(2,1));
    alpha = atan2(ooi_measured(2,1),ooi_measured(1,1));
    range = sqrt(ooi_measured(2,1)^2+ooi_measured(1,1)^2);
    yk = [range;alpha];
   
    xs = est_pose(1)+0.4*cos(est_pose(3));
    ys = est_pose(2)+0.4*sin(est_pose(3));
    
   hk = [sqrt((landmark(1)-(xs))^2 +(landmark(2)-(ys))^2);atan2(landmark(2)-ys,landmark(1)-xs)-est_pose(3)];
   z_k = yk - hk;
   z_k(2,1) = wrapToPi(z_k(2,1));
   
   %Innovation Covariance
   H_k_wrt =  [-(landmark(1)-xs)/(sqrt((landmark(1)-xs)^2 +(landmark(2)-ys)^2)),-(landmark(2)-ys)/(sqrt((landmark(1)-xs)^2 +(landmark(2)-ys)^2)),0,0;
   
   (landmark(2)-ys)/((landmark(1)-xs)^2 +(landmark(2)-ys)^2),((-1)*(landmark(1)-xs))/((landmark(1)-xs)^2 +(landmark(2)-ys)^2),-1,0
   ];
   R = [0.1^2,0;0,(2*pi/180)^2] ;

   Sk = H_k_wrt*p_k*H_k_wrt' + R;
   
   i_s = inv(Sk);
   Kal = (p_k*H_k_wrt')*i_s;
    
   ekf_pose = est_pose + Kal*z_k;
   ekf_var = p_k-p_k*Kal*H_k_wrt;
   
end

function plot_ugv(ph, pose)
    set(ph(1), 'xdata', pose(1), 'ydata', pose(2));
    heading = [pose(1), 3*cos(pose(3))+pose(1); pose(2), 3*sin(pose(3))+pose(2)];
    set(ph(3), 'xdata', heading(1, :), 'ydata', heading(2, :));
end

 %calculate bias
 
 
 
 
function [pp,ooi] = processLiDAR(ranges,API) %part b
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
    [~,~,rrc,aac] = API.FindSegments(rr,0.8);   % discontinuity: d>0.8m

    xx = rrc.*cos(aac);
    yy = rrc.*sin(aac);
    ooi = [xx; yy];


    
    
    


    % shown in local CF.
% You may introduce a delay (using pause(...) ), here; if we are showing some dynamic plots.









end


function [landmarks_for_tri,ooi_local] = data_assoc(pp,ph,X,etc,ooi,Landmarks,API) %part C
    %move to ugv pov
    ooi_copy = ooi;
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
   
    
    
    [~,~,iiO,uuL]=API.DA( ooi(1,:),ooi(2,:),Landmarks(1,:), Landmarks(2,:), 0.3);

    ooi_local = ooi_copy(:,iiO);

    landmarks_for_tri = Landmarks(:,uuL);
    [~,ncols] = size(ooi);

    set(ph(2), 'xdata', pp(1, :), 'ydata', pp(2, :));
    if ncols > 0
        set(ph(4), 'xdata', ooi(1, iiO), 'ydata', ooi(2, iiO));
    end
    
    
end


% 
% function estposition = Trilateration(landmarks_for_tri,ooi_local,prev_pose) %part D
%         [~,ncols] = size(landmarks_for_tri);
%         z = prev_pose;
%         x0 = [double(prev_pose(1,1)),double(prev_pose(1,2)),double(prev_pose(1,3))];
%         if ncols > 2
%             [bearing1,range1] = cart2pol(ooi_local(1,1),ooi_local(2,1));
%             [bearing2,range2] = cart2pol(ooi_local(1,2),ooi_local(2,2));
%             fun = @(x) [double(range1) - sqrt((x(1)-double(landmarks_for_tri(1,1)))^2 +(x(2)-double(landmarks_for_tri(2,1)))^2 );
%                 double(range2) - sqrt((x(1)-double(landmarks_for_tri(1,2)))^2 +(x(2)-double(landmarks_for_tri(2,2)))^2 ) ;
% 
%                 double(bearing1) - atan2(double(landmarks_for_tri(2,1))-x(2),double(landmarks_for_tri(1,1))-x(1)) + x(3);
%                 double(bearing2) - atan2(double(landmarks_for_tri(2,2))-x(2),double(landmarks_for_tri(1,2))-x(1)) + x(3);
%                 
%                 ];
%             z = fsolve(fun,x0);
%             x0 = z;
%             for i = 3:ncols
%             [bearing,range] = cart2pol(ooi_local(1,i),ooi_local(2,i));
%             fun = @(x) [double(range) - sqrt((x(1)-double(landmarks_for_tri(1,i)))^2 +(x(2)-double(landmarks_for_tri(2,i)))^2 );
%             double(bearing) - atan2(double(landmarks_for_tri(2,i))-x(2),double(landmarks_for_tri(1,i))-x(1)) + x(3)
%             ];
%             z = lsqnonlin(fun,x0); 
%             end
%         end
%         
%         estposition = z;
% 
% end



% if you have questions, ask the lecturer, via Moodle or email(
% j.guivant@unsw.edu.au)
% or ask the demonstrators.
