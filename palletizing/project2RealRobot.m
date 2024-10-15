% 
clc;
clear all;

% TCP Host and Port settings
host = '192.168.0.100'; % THIS IP ADDRESS MUST BE USED FOR THE REAL ROBOT
rtdeport = 30003;
vacuumport = 63352;

% Calling the constructor of rtde to setup tcp connction
rtde = rtde(host,rtdeport);

home = [-600,-200,70,2.2214, -2.2214, 0.00];

rtde.movel(home);   
% Calling the constructor of vacuum to setup tcp connction
vacuum = vacuum(host,vacuumport);

totalNparcels = 5;


% TODO  
% Call another function here.
%[parcel_1,parcel_2,parcel_3,parcel_4,parcel_5]\
%for video desiredPos = [2,2,4,4,3]

desiredPos = [2,2,4,4,3]
global currPos
currPos = [1,1,1,1,1];
[aux1,aux2] = getAuxboxes(currPos(totalNparcels),desiredPos(totalNparcels));
moveAlgo(totalNparcels,currPos(totalNparcels),desiredPos(totalNparcels),aux1,aux2,desiredPos,totalNparcels,rtde,vacuum)

for k = totalNparcels-1:-1:1
    if(desiredPos(k) ~= desiredPos(k+1))
        [aux1,aux2] = getAuxboxes(currPos(k),desiredPos(k));
        moveAlgo(k,currPos(k),desiredPos(k),aux1,aux2,desiredPos,totalNparcels,rtde,vacuum)
    end
end
%     [aux1,aux2] = getAuxboxes(sim.currentPos(5),desiredPos(5))
%     moveAlgo(5,sim.currentPos(5),desiredPos(5),aux1,aux2,sim,desiredPos);
% The following move function is an example. Feel free to replace it.
%move(sim);
currPos
disp("Finished")


function h = getHeight(box,totalNparcels)  
    h = 0;    
    global currPos
    for i = 1:totalNparcels
        if box == currPos(i)
            h = h + 1;
        end
    end
    h = h*3;
end

function c = getcurrentBox(parcel,totalNparcels)
    global currPos
    c = currPos(parcel);
end

function p = topofbox(box,totalNparcels)
    p = 0;
    global currPos

    for i = 1:totalNparcels
        if currPos(i) == box
            p = i;
            return
        end
    end
end

function pose = boxtocoords(box)
    if box == 1
        pose = [-700,-100,60,2.2214, -2.2214, 0.00];
    end
    if box == 2
        pose = [-500,-100,60,2.2214, -2.2214, 0.00];
    end
    if box == 3
        pose = [-700,-300,60,2.2214, -2.2214, 0.00];
    end
    if box == 4
        pose = [-500,-300,60,2.2214, -2.2214, 0.00];
    end

end

function movesrctodest(src,dest,totalNparcels,rtde,vacuum);
    %change currPos
    global currPos
    p = topofbox(src,totalNparcels);
    currPos(p) = dest;
    h_src = getHeight(src,totalNparcels);
    h_dest = getHeight(dest,totalNparcels);
    a = 1.0;
    v = 0.07;
    r = 0;

    src = boxtocoords(src);
    dest = boxtocoords(dest);


    rtde.movel(src,'pose',a,v,r);
    src(3) = h_src;
    rtde.movel(src,'pose',a,v,r);
    vacuum.grip()
    src(3) = 60;
    rtde.movel(src,'pose',a,v,r);
    
    
    %drop
    rtde.movel(dest,'pose',a,v,r);
    dest(3) = h_dest;
    rtde.movel(dest,'pose',a,v,r);
    vacuum.release()
    pause(0.2)
    dest(3) = 60;
    rtde.movel(dest,'pose',a,v,r);
    


    
end


function bool = isSolved(desiredPos)
    bool = 0;
    global currPos
    currentPos = currPos;
    if currentPos(1) == desiredPos(1) && currentPos(2) == desiredPos(2) && currentPos(3) == desiredPos(3) && currentPos(4) == desiredPos(4) && currentPos(5) == desiredPos(5) 
    bool = 1;
    end
end

function [aux1,aux2] = getAuxboxes(src,dest)
    aux1 = -1;
    aux2 = -1;

    for i = 1:4
        if(i ~= src && i ~= dest )
            aux1 = i;
        end
    end

    for i = 1:4
        if(i ~= aux1 && i ~= src && i ~= dest )
            aux2 = i;
        end
    end

end

function moveAlgo(parcel,src,dest,aux1,aux2,desiredPos,totalNparcels,rtde,vacuum)
    bool = isSolved(desiredPos);  
    if parcel == 0 || bool == 1
        disp("End") 
        return 
    end
    if (parcel == 1) 
        movesrctodest(src,dest,totalNparcels,rtde,vacuum);
        return
    end

    moveAlgo(parcel - 2, src, aux1, aux2,dest,desiredPos,totalNparcels,rtde,vacuum);
    movesrctodest(src,aux2,totalNparcels,rtde,vacuum);
    movesrctodest(src,dest,totalNparcels,rtde,vacuum);
    movesrctodest(aux2,dest,totalNparcels,rtde,vacuum);
    moveAlgo(parcel - 2, aux1, dest, src,aux2,desiredPos,totalNparcels,rtde,vacuum);
    
end