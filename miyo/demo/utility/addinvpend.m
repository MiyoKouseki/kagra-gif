%% main

function sus=addinvpend(sus,bodyB,bodyS,loadip,radip,lenip,freq,Q,cop,ktor)

% addinvpend adds a connection of inverted pendulum between two rigid-bodies.
% Following input arguments are required:
%   sus   : suspension sturcture
%   bodyB : base body name
%   bodyS : upper body name
%   load  : total load on IP [kg]
%   radius: distance between IP legs and center of mass
%   length: Length of IP leg [m]
%   freq  : resonant frequency about translation mode [Hz]
%   Q     : quality factor
%   cop   : Saturation level due to CoP effect
%   ktor  : additional torsional stiffness by flexures [N*m/rad]

% input check
checkinput(sus,bodyB,bodyS,loadip,radip,lenip,freq,Q,cop,ktor);

% IP

if ~isfield(sus,'i')
    sus.i.bb={};
    sus.i.sb={};
    sus.i.m ={};
    sus.i.r ={};
    sus.i.l ={};
    sus.i.f ={};
    sus.i.Q ={};
    sus.i.cp={};
    sus.i.kt={};
end

sus.i.bb=[sus.i.bb,bodyB];
sus.i.sb=[sus.i.sb,bodyS];
sus.i.m =[sus.i.m ,loadip];
sus.i.r =[sus.i.r ,radip];
sus.i.l =[sus.i.l ,lenip];
sus.i.f =[sus.i.f ,freq];
sus.i.Q =[sus.i.Q ,Q];
sus.i.cp=[sus.i.cp,cop];
sus.i.kt=[sus.i.kt,ktor];

end

function checkinput(sus,bodyB,bodyS,loadip,radip,lenip,freq,Q,cop,ktor)

if ~isstruct(sus)
    error('addinvpend:InputError',...
        'First argument [sus] must be a structure with a name specified.')
end

if ~isfield(sus,'n')
    error('addinvpend:InputError',...
        'First argument [sus] must be a structure with a name specified.')
end

if ~isfield(sus,'b')
    error('addinvpend:InputError',...
        'Rigid bodies must be registrated before wires are added.')
end

if ~isfield(sus,'g')
    error('addinvpend:InputError',...
        'Grounds must be registrated before wires are added.')
end

bn=[sus.b.n,sus.g.n]; % body name list

if ~ischar(bodyB)
    error('addinvpend:InputError',...
        'Second argument [bodyB] must be a body name.')
end

if isempty(bn(strcmp(bodyB,bn)))
    error('addinvpend:InputError',...
        'Second argument [bodyB] must be a body name.')
end

if ~ischar(bodyS)
    error('addinvpend:InputError',...
        'Third argument [bodyS] must be a body name.')
end

if isempty(bn(strcmp(bodyS,bn)))
    error('addinvpend:InputError',...
        'Third argument [bodyS] must be a body name.')
end

if ~isreal(loadip)
    error('addinvpend:InputError',...
        'Forth argument [load] must be a real number.')
end

if length(loadip)~=1
    error('addinvpend:InputError',...
        'Forth argument [load] must be a real number.')
end

if ~isreal(radip)
    error('addinvpend:InputError',...
        'Fifth argument [radius] must be a real number.')
end

if length(radip)~=1
    error('addinvpend:InputError',...
        'Fifth argument [radius] must be a real number.')
end

if ~isreal(lenip)
    error('addinvpend:InputError',...
        'Sixth argument [lenip] must be a real number.')
end

if length(lenip)~=1
    error('addinvpend:InputError',...
        'Sixth argument [lenip] must be a real number.')
end

if ~isreal(freq)
    error('addinvpend:InputError',...
        'Seventh argument [freq] must be a real number.')
end

if length(freq)~=1
    error('addinvpend:InputError',...
        'Seventh argument [freq] must be a real number.')
end

if ~isreal(Q)
    error('addinvpend:InputError',...
        'Eighth argument [Q] must be a real number.')
end

if length(Q)~=1
    error('addinvpend:InputError',...
        'Eighth argument [Q] must be a real number.')
end

if ~isreal(cop)
    error('addinvpend:InputError',...
        'Ninth argument [cop] must be a real number.')
end

if length(cop)~=1
    error('addinvpend:InputError',...
        'Ninth argument [cop] must be a real number.')
end

if ~isreal(ktor)
    error('addinvpend:InputError',...
        'Tenth argument [ktor] must be a real number.')
end

if length(cop)~=1
    error('addinvpend:InputError',...
        'Tenth argument [ktor] must be a real number.')
end

end