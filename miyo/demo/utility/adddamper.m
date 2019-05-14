%% main

function sus=adddamper(sus,body1,body2,pos1,pos2,dampmat)

% adddamper adds a viscous-dapmper between two rigid-bodies.
% Following input arguments are required:
%   sus: suspension sturcture
%   body1: upper body name
%   body2: lower body name
%   pos1:  damping point about upper body from CoM
%   pos2:  damping point about upper body from CoM
%   dampmat: damping coefficient matrix [6x6]


% input check
checkinput(sus,body1,body2,pos1,pos2,dampmat);

if ~isfield(sus,'d')
    sus.d.b1={};
    sus.d.b2={};
    sus.d.p1={};
    sus.d.p2={};
    sus.d.m ={};
end

sus.d.b1=[sus.d.b1, body1];
sus.d.b2=[sus.d.b2, body2];
sus.d.p1=[sus.d.p1, pos1];
sus.d.p2=[sus.d.p2, pos2];
sus.d.m =[sus.d.m , dampmat];

end

%% checkinput
function checkinput(sus,body1,body2,pos1,pos2,dampmat)
if ~isstruct(sus)
    error('adddamper:InputError',...
        'First argument [sus] must be a structure with a name specified.')
end

if ~isfield(sus,'n')
    error('adddamper:InputError',...
        'First argument [sus] must be a structure with a name specified.')
end

if ~isfield(sus,'b')
    error('adddamper:InputError',...
        'Rigid bodies must be registrated before wires are added.')
end

if ~isfield(sus,'g')
    error('adddamper:InputError',...
        'Grounds must be registrated before wires are added.')
end

bn=[sus.b.n,sus.g.n]; % body name list

if ~ischar(body1)
    error('adddamper:InputError',...
        'Second argument [body1] must be a body name.')
end

if isempty(bn(strcmp(body1,bn)))
    error('adddamper:InputError',...
        'Second argument [body1] must be a body name.')
end

if ~ischar(body2)
    error('adddamper:InputError',...
        'Third argument [body2] must be a body name.')
end

if isempty(bn(strcmp(body2,bn)))
    error('adddamper:InputError',...
        'Third argument [body2] must be a body name.')
end

if ~isreal(pos1)
    error('adddamper:InputError',...
        'Forth argument [pos1] must be a vector of real numbers.')
end

if length(pos1)~=3
    error('adddamper:InputError',...
        'Forth argument [pos1] must be a vector with 3 elements.')
end

if ~isreal(pos2)
    error('adddamper:InputError',...
        'Fifth argument [pos2] must be a vector of real numbers.')
end

if length(pos2)~=3
    error('adddamper:InputError',...
        'Fifth argument [pos2] must be a vector with 3 elements.')
end

if ~ismatrix(dampmat)
    error('adddamper:InputError',...
        'Sixth argument [dampmat] must be a 6x6 matrix.')
end

if ~(size(dampmat,1)==6 && size(dampmat,2)==6)
    error('adddamper:InputError',...
        'Sixth argument [dampmat] must be a 6x6 matrix.')
end

end