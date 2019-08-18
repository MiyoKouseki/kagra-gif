%% main

function sus=addsuswire(sus,num,opt,body1,body2,geoparam,len,...
    diameter,load,young,shear,Q,varargin)

% addsuswire function adds a wire connection between two rigid bodies.
% Following input arguments are required:
% 
% #01 sus      : suspension structure
%   The argument must be a structure specifying a suspension model.
%   Grounds and rigid bodies are to be registered beforehand.
% 
% #02 num      : number of wires
%   The argument specifies a number of wires connecting two bodies.
%   It must be an integer between 1 and 4.
% 
% #03 opt      : options
%   The argument must be a cell array of strings specifying option names
%   for the calculation. Following options are available:
% 
%   'neck': Each wire possesses neck parts in the both ends which have
%           different diameter from that of the central part. When this
%           option is specified, one has to specify two different diameters
%           of the neck parts and the central part in #09 argument [len].
%           One also has to specify the length of the neck parts in
%           #08 argument [diameter].
% 
%   'spring': A vertical spring is placed in one end of each wire. When
%             this option is specified, one has to add an argument in the
%             last argument [varargin] to specify the parameters.
% 
%   'nobend': Bending point shifts due to the bending stiffness of the wires
%             are ignored when this option is specified. So the bending
%             points and suspension points coincide in the model.
% 
% #04 body1    : upper body name
% #05 body2    : lower body name
%   These arguments specify the names of rigid bodies to which the wires are
%   attached. They must be selected from the ground or rigid body names.
% 
% #06 geoparam : geometric parameters
%   The argument specifies parameters about the geometry of the suspension.
%   It must be a vector of real numbers. Required number of parameters
%   depends on the number of suspension wires (#02 [num]). All the values
%   of the parameters have units of [m].
% 
%   num=1 --> geoparam = [h1, h2];
%   num=2 --> geoparam = [h1, h2, w1];
%   num=3 --> geoparam = [h1, h2, r1];
%   num=4 --> geoparam = [h1, h2, w1, d1];
% 
%       h1: Vertical position of the upper suspension points from the center
%           of mass of the upper body. When the value is positive, the
%           suspension point is higher than the center of mass.
%       h2: Vertical position of the lower suspension points from the center
%           of mass of the lower body. When the value is positive, the
%           suspension point is higher than the center of mass.
%       r1: Horizontal distance between the upper suspension points of
%           wires and the center of mass of the upper body.
%      (r2: Horizontal distance between the lower suspension points of
%           wires and the center of mass of the lower body.)
%       w1: Separation of upper suspesnion points and the center of mass
%           of the upper body in the transversal direction.
%      (w2: Separation of lower suspesnion points and the center of mass
%           of the lower body in the transversal direction.)
%       d1: Separation of upper suspesnion points and the center of mass
%           of the upper body in the longitudinal direction.
%      (d2: Separation of lower suspesnion points and the center of mass
%           of the lower body in the longitudinal direction.)
%    Without any special options, we assume that wires are vertical
%    in the calm state. i.e. r1=r2, w1=w2, d1=d2
% 
% #07 len      : length
%   The argument specifies the lengths of the wires in [m]. It must be a
%   single real number unless any special options are specified.
%   When the option 'neck' is specified in argument #03 [opt], it must be a 
%   vector of two real numbers. The first value specfies the length of the
%   wire (L) and the second value specifies the length of a neck part(Ln).
%   The length of the central part becomes Lc=L-2*Ln.
% 
% #08 diameter : diameter
%   The argument specifies the daimeters of the wires in [m]. It must be a
%   single real number unless any special options are specified.
%   When the option 'neck' is specified in argument #03 [opt], it must be a 
%   vector of two real numbers. The first value specfies the diameter of the
%   wire (D) and the second value specifies the diameter of neck parts(Dn).
% 
% #09 load     : total load on wires
%   The argument specifies the total load on the suspension wires in [kg].
%   It must be a single real number. In a symmetric system,
%   the tension on each wire is calculated as T=M*g/n/cos(t),
%   where M is the specified load, g is the gravity constant,
%   n is the number of wires, and t is the angle of the wire from the
%   vertical axis.
% 
% #10 young    : Young's modulus
%   The argument specifies the Young's modulus of the wire material in
%   [Pa]. It must be a single real number. The tensile stiffness of the
%   wire is basically calculated as ks=E*d^2*pi/4/L [N/m],
%   where E is the specified Young's modulus, d is the wire diameter,
%   and L is the wire length.
% 
% #11 shear    : shear modulus
%   The argument specifies the shear modulus of the wire material in
%   [Pa]. It must be a single real number. The torsional stiffness of the
%   wire is basically calculated as kt=G*d^4*pi/32/L [M*m/rad],
%   where G is the specified shear modulus, d is the wire diameter,
%   and L is the wire length.
% 
% #12 Q         : Quality factor
%   The argument specifies the quality factor of the wire material.
% 
% #13~ varargin : Arbitrary input arguments
%   The arguments are required when special options are specified in the
%   argument #03 [opt]. Each argument must be a cell array of strings or
%   numbers. The first element of the cell must declair the content you
%   you want to specify in the argument. The folloiwng argumnets can be
%   described:
%   
%   'spring': The argument is required when the 'spring' option is specified
%             in the argument #03 [opt]. The argument should be in the 
%             following format: {'spring', fsp, Bsp, Qsp};
%             fsp: Resonant frequency of the spring
%             Bsp: Saturation level of the vibration isolation ratio due
%                  to the center of percussion (CoP) effect
%             Qsp: Q factor of the spring

    checkinput(sus,num,opt,body1,body2,geoparam,len,...
    diameter,load,young,shear,Q,varargin);

if ~isfield(sus,'w')
    sus.w.n ={};
    sus.w.op={};
    sus.w.ub={};
    sus.w.lb={};
    sus.w.g ={};
    sus.w.l ={};
    sus.w.d ={};
    sus.w.t ={};
    sus.w.y ={};
    sus.w.s ={};
    sus.w.Q ={};
    sus.w.ai={};
end


% WIRE
sus.w.n =[sus.w.n, num];      % number of wires
sus.w.op=[sus.w.op,{opt}];    % option
sus.w.ub=[sus.w.ub,body1];    % upper body name
sus.w.lb=[sus.w.lb,body2];    % lower body name
sus.w.g =[sus.w.g, geoparam]; % geometric parameters
sus.w.l =[sus.w.l, len];      % length
sus.w.d =[sus.w.d, diameter]; % diameter
sus.w.t =[sus.w.t, load];     % total weight applied on wires
sus.w.y =[sus.w.y, young];    % young's modulus
sus.w.s =[sus.w.s, shear];    % shear modulus
sus.w.Q =[sus.w.Q, Q];    % Q factor
sus.w.ai=[sus.w.ai,{varargin}]; % arbitorary inputs

end



%% checkinput

function checkinput(sus,num,opt,body1,body2,geoparam,len,...
    diameter,load,young,shear,Q,varargin0)

% input error check

opl={'nobend','spring','neck'}; % list of options

% #01 sus
if ~isstruct(sus)
    error('addsuswire:InputError',...
        'First argument [sus] must be a structure with a name specified.')
end

if ~isfield(sus,'n')
    error('addsuswire:InputError',...
        'First argument [sus] must be a structure with a name specified.')
end

if ~isfield(sus,'b')
    error('addsuswire:InputError',...
        'Rigid bodies must be registrated before wires are added.')
end

if ~isfield(sus,'g')
    error('addsuswire:InputError',...
        'Grounds must be registrated before wires are added.')
end

% #02 num
if ~isreal(num)
    error('addsuswire:InputError',...
        'Second argument [num] must be an integer between 1 and 4.')
end

if ~(num==1||num==2||num==3||num==4)
    error('addsuswire:InputError',...
        'Second argument [num] must be an integer between 1 and 4.')
end

% #03 opt

if ~iscellstr(opt)
    error('addsuswire:InputError',...
        'Third argument [opt] must be a cell array of strings.')
end

oplf=strjoin(opl,''', ''');

if ~isempty(opt)
    nop=numel(opt);
    for n=1:nop
        if isempty(opl(strcmp(opt{n},opl)))
           error('addsuswire:InputError',...
        ['''',opt{n},''' is not a proper option name. ',...
        'Possible options are:\n''',oplf,''''])
        end
    end 
end

% #04 body1

bn=[sus.b.n,sus.g.n]; % body name list

if ~ischar(body1)
    error('addsuswire:InputError',...
        'Forth argument [body1] must be a body name.')
end

if isempty(bn(strcmp(body1,bn)))
    error('addsuswire:InputError',...
        'Forth argument [body1] must be a body name.')
end

% #05 body2

if ~ischar(body2)
    error('addsuswire:InputError',...
        'Fifth argument [body2] must be a body name.')
end

if isempty(bn(strcmp(body2,bn)))
    error('addsuswire:InputError',...
        'Fifth argument [body2] must be a body name.')
end

% #06 geoparam

if ~isvector(geoparam)
    error('addsuswire:InputError',...
        'Sixth argument [geoparam] must be a vector of real numbers.')
end

if ~isreal(geoparam)
    error('addsuswire:InputError',...
        'Sixth argument [geoparam] must be a vector of real numbers.')
end

if (num==1 && length(geoparam)~=2)||...
        (num==2 && length(geoparam)~=3)||...
        (num==3 && length(geoparam)~=3)||...
        (num==4 && length(geoparam)~=4)
    error('addsuswire:InputError',...
        'Sixth argument [geoparam] have wrong length.')
end

% #07 len

if isempty(opt(strcmp('neck',opt)))
    if ~isreal(len)
        error('addsuswire:InputError',...
            'Seventh argument [len] must be a real number.')
    end
    if length(len)~=1
        error('addsuswire:InputError',...
            'Seventh argument [len] must be a real number.')
    end
    
else
    if ~isreal(len)
        error('addsuswire:InputError',...
            ['Seventh argument [len] must be a vector of two real numbers ',...
            'when the option ''neck'' is specified.'])
    end
    if length(len)~=2
        error('addsuswire:InputError',...
            ['Seventh argument [len] must be a vector of two real numbers ',...
            'when the option ''neck'' is specified.'])
    end
    
end

% #08 diameter

if isempty(opt(strcmp('neck',opt)))
    if ~isreal(diameter)
        error('addsuswire:InputError',...
            'Eighth argument [diameter] must be a real number.')
    end
    
    if length(diameter)~=1
        error('addsuswire:InputError',...
            'Eighth argument [diameter] must be a real number.')
    end
    
else
    if ~isreal(diameter)
        error('addsuswire:InputError',...
            ['Eighth argument [diameter] must be a vector of two real numbers ',...
            'when the option ''neck'' is specified.'])
    end
    if length(diameter)~=2
        error('addsuswire:InputError',...
            ['Eighth argument [diameter] must be a vector of two real numbers ',...
            'when the option ''neck'' is specified.'])
    end
    
end

% #09 load

if ~isreal(load)
    error('addsuswire:InputError',...
        'Ninth argument [load] must be a real number.')
end

if length(load)~=1
    error('addsuswire:InputError',...
        'Ninth argument [load] must be a real number.')
end

% #10 young

if ~isreal(young)
    error('addsuswire:InputError',...
        'Tenth argument [young] must be a real number.')
end

if length(young)~=1
    error('addsuswire:InputError',...
        'Tenth argument [young] must be a real number.')
end

% #11 shear

if ~isreal(shear)
    error('addsuswire:InputError',...
        'Eleventh argument [shear] must be a real number.')
end

if length(shear)~=1
    error('addsuswire:InputError',...
        'Eleventh argument [shear] must be a real number.')
end

% #12 Q

if ~isreal(Q)
    error('addsuswire:InputError',...
        'Twelfth argument [Q] must be a real number.')
end

if length(Q)~=1
    error('addsuswire:InputError',...
        'Twelfth argument [Q] must be a real number.')
end

% #13 varargin

if ~isempty(opt(strcmp('spring',opt))) % option 'spring'
    if isempty(varargin0)
        error('addsuswire:InputError',...
             'No arguments describing spring parameters are found.')
    end
    if ~iscell(varargin0{1})
        error('addsuswire:InputError',...
             'Wrong argument in [varargin].')
    end
    
    na0=length(varargin0);
    nvlst=cell(na0);
    for n=1:na0
        if ~ischar(varargin0{n}{1})
            error('addsuswire:InputError',...
             'First element of [varargin] must be a string.')
        else
            nvlst{n}=varargin0{n}{1};
        end
    end
    if isempty(varargin0(strcmp('spring',nvlst)))
        error('addsuswire:InputError',...
             'No arguments describing ''spring'' parameters are found.')
    end
    argspr=varargin0{strcmp('spring',nvlst)};
    if length(argspr)~=4
        error('addsuswire:InputError',...
             'Wrong argument in ''spring'' parameters.')
    end
    if ~isreal(argspr{2})||~isreal(argspr{3})||~isreal(argspr{4})
        error('addsuswire:InputError',...
             'Wrong argument in ''spring'' parameters.')
    end
    
    % possible other options here:
    
    
    
else
    if ~isempty(varargin0)
        error('addsuswire:InputError',...
             'Too many input arguments.')
    end
end


end
