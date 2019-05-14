
%% main

function sus=addrigidbody(sus,name,mass,moi)
% addrigidbody function registrates a rigid body to the structure

checkinput(sus,name,mass,moi);

if ~isfield(sus,'b')
    sus.b.n={};
    sus.b.m={};
    sus.b.I={};
end

sus.b.n=[sus.b.n, name];
sus.b.m=[sus.b.m, mass];
sus.b.I=[sus.b.I, moi];

end



%% checkinput

function checkinput(sus,name,mass,moi)
% input error check

if ~isstruct(sus)
    error('addrigidbody:InputError',...
        'First argument must be a structure with a name specified.')
end

if ~isfield(sus,'n')
    error('addrigidbody:InputError',...
        'First argument must be a structure with a name specified.')
end

if ~ischar(name)
    error('addrigidbody:InputError',...
        'Second argument must be a string.')
end

if ~isreal(mass)
    error('addrigidbody:InputError',...
        'Third argument must be a positive number.')
end

if mass<=0
    error('addrigidbody:InputError',...
        'Third argument must be a positive number.')
end

if ~ismatrix(moi)
    error('addrigidbody:InputError',...
        'Forth argument must be a 3x3 matrix.')
end

if ~(size(moi,1)==3 && size(moi,2)==3)
    error('addrigidbody:InputError',...
        'Forth argument must be a 3x3 matrix.')
end

end