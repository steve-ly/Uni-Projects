%--------------------------------------------------
% This program shows how to use the provided API, for performing detection
% of OOIs, and to perform Data Association of those OOIs and map landmarks.
% the API is intended to be used by students who have not been able to
% implement similar functions in Project 1 parts B and C.
%--------------------------------------------------
% note: 
% this API's functions can be called as many times you want, from your program,
% but every 200  calls the API will open a message box to inform tutors 
% that your program is using  the API. To continue working, when the message box does appear, just press the 
% "OK" button in the message box.
%--------------------------------------------------
% Questions: ask the lecturer, j.guivant@unsw.edu.au
%--------------------------------------------------

function main()
% First, open API, just once is enough.
AA=API_project1_AAS();

%We try it, with with some LiDAR scan data and some Landmarks map.
FileNameLidarScan='.\LiDAR_data_002.mat';
FileNameLandmarksMap='./ManyPoles01.mat';

ExampleTestThisScan(FileNameLidarScan,FileNameLandmarksMap,AA);
end
% .................................................

function ExampleTestThisScan(file,fileMap,API)
a = [-80:0.5:80]*pi/180;

load(file) ;  %load 1 LiDAR scan data
ranges = single(Scan.ranges)*0.01      % in metres

% Call API function, for performing OOI detection.
[iiFirst,iiLast,rrc,aac] = API.FindSegments(ranges,0.8);   % discontinuity: d>0.8m

% ------------------------- plot result
figure(1); clf();
plot(a,ranges,'b.');hold on;

 plot(aac,rrc,'or');
 plot(a(iiFirst),ranges(iiFirst),'r.');
 plot(a(iiLast),ranges(iiLast),'.g');
% 
legend({'LiDAR scan points','approx. CoGs','first pixels','last pixels'});
title('testing API pole detector');
xlabel('angle (rad)');ylabel('range (m)');
%-------------------------

% Test Data Association (DA)

% approx. OOIs' centres in LiDAR CF, in Cartesian representation.
xx= rrc.*cos(aac); 
yy= rrc.*sin(aac);
X=Scan.X; % LiDAR's pose when the scan was taken

c=cos(X(3));  s=sin(X(3)); R=  [  [c,-s];[s,c]];  % rotation matrix
pp = [xx;yy]
R
pp=R*pp;
pp(1,:)=pp(1,:)+X(1);
pp(2,:)=pp(2,:)+X(2);
% convert approx OOI's positions from LiDAR CF to GCF.

% here, we some perturbation, just to test DA
pp=pp+2*0.6*( rand(size(pp))-0.5);


% load Map of Landmarks, to test the DA API function
load(fileMap);
Landmarks=Poles.XY(:,1:2)';


% perform DA, using API.
[~,~,iiO,uuL]=API.DA( pp(1,:),pp(2,:),Landmarks(1,:), Landmarks(2,:), 0.9);
iiO
uuL

% ......................................
% some plot, for visual verification.
figure(3); clf();
plot(Landmarks(1,:), Landmarks(2,:),'+');
hold on;
plot(pp(1,:),pp(2,:),'or');


API.PlotCouples(pp(:,iiO),Landmarks(:,uuL),3,'m');
legend({'Set A','Set B','Association'});
title('testing API Data Association');
xlabel('x (m)');ylabel('y (m)');
% done.
end
%.............................................