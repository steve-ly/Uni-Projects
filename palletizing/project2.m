% DO NOT CHANGE THE FILE NAME OR IT WILL NOT WORK DURING TESTING
% Author: 
% zid:
% Date:

% DO NOT CHANGE THE FUNCTION DEFINITION. OR IT WILL FAIL THE TESTS
% You are welcome to call other functions from this main function.
function sim = project2(desiredPosition, totalNumberOfParcesl, pauseTime)
    % This line needs to be the very first line. Do not remove it.
    sim = project2simulator(totalNumberOfParcesl,pauseTime);
    n = totalNumberOfParcesl;
    

    % TODO  
    % Call another function here.
    desiredPos = getDesiredPos(desiredPosition)
    %find stacks
    if (n <= 3)
         isUnique = individualBox(desiredPos,n);
         if isUnique == 1;
             for k = 1:n
                 movesrctodest(sim.currentPos(k),desiredPos(k),sim);
             end
         end
    end



    [aux1,aux2] = getAuxboxes(sim.currentPos(n),desiredPos(n));
    moveAlgo(n,sim.currentPos(n),desiredPos(n),aux1,aux2,sim,desiredPos);

    for k = n-1:-1:1
        if(desiredPos(k+1) ~= desiredPos(k))
        [aux1,aux2] = getAuxboxes(sim.currentPos(k),desiredPos(k));
        moveAlgo(k,sim.currentPos(k),desiredPos(k),aux1,aux2,sim,desiredPos);
        end
    end
%     [aux1,aux2] = getAuxboxes(sim.currentPos(5),desiredPos(5))
%     moveAlgo(5,sim.currentPos(5),desiredPos(5),aux1,aux2,sim,desiredPos);
    % The following move function is an example. Feel free to replace it.
    %move(sim);
    disp("Finished")
    
end

function desiredPos = getDesiredPos(desiredPosition)
    desiredPos = [0,0,0,0,0];
    rows = 4;   
    cols = 5;
    for i = 1:rows
        for j = 1:cols
            x = desiredPosition(i,j);
            if x > 0
                desiredPos(x) = i;
            end
        end
    end
end


function movesrctodest(src,dest,sim)
    sim.pickup(src);
    sim.putdown(dest);
end


function bool = isSolved(sim,desiredPos)
    bool = 0;
    if sim.currentPos(1) == desiredPos(1) && sim.currentPos(2) == desiredPos(2) && sim.currentPos(3) == desiredPos(3) && sim.currentPos(4) == desiredPos(4) && sim.currentPos(5) == desiredPos(5) 
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

function moveAlgo(parcel,src,dest,aux1,aux2,sim,desiredPos)
    bool = isSolved(sim,desiredPos);  
    if parcel == 0 || bool == 1
        return 
    end
    if (parcel == 1) 
        movesrctodest(src,dest,sim)
        return
    end

    moveAlgo(parcel - 2, src, aux1, aux2,dest,sim,desiredPos);
    movesrctodest(src,aux2,sim);
    movesrctodest(src,dest,sim);
    movesrctodest(aux2,dest,sim);
    moveAlgo(parcel - 2, aux1, dest, src,aux2,sim,desiredPos);
    
end

function isUnique = individualBox(desiredPos,n)
    isUnique = 1;
    boxes = [0,0,0,0];
    for i = 1:n
        boxes(desiredPos(i)) = boxes(desiredPos(i)) + 1;
    end
    for j = 1:4
        if boxes(j) > 1
            isUnique = 0;
        end
    end
end




% This is just an example function to show the functionality of the
% project2simulator
