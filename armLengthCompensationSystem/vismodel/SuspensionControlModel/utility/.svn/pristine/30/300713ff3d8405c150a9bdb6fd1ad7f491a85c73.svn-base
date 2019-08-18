function matKwn=makematKwn1(wten,wln,wh1n,wh2n,weffbn,wQn,wQsn,wksn,wktn)

% makematKwn1 calculates the stiffness matrix of a single wire suspension.
% Following arguments are required;
%   wten: tension on a wire [N]
%   wln:  wire length
%   wh1n: vertical position of upper suspension point from center of mass
%         of the upper body
%   wh2n: vertical position of lower suspension point from center of mass
%         of the lower body
%   wQn:  Quality factor of wire material
%   wQsn: Quality factor of bounce mode (spring mode)
%   wksn: Spring constant about bouce mode [N/m]
%   wksn: Spring constant about torsion mode [N*m/rad]

wnn = 1; % number of wires
matKwn=zeros(12,12);

delta=weffbn*(1+1i/wQn/2); % complex bending length
wh1neff=wh1n-delta;        % upper effective bending point
wh2neff=wh2n+delta;        % lower effective bending point
wlneff =wln-2*delta;       % effective wire length

% Longitudinal-Pitch
matLP=wten*wnn/wlneff*...
    [ 1,      +wh1neff,       -1,      -wh2neff;...
    +wh1neff, -wh1neff*(wlneff-wh1neff), -wh1neff,   -wh1neff*wh2neff;...
    -1,       -wh1neff,        1,      +wh2neff;...
    -wh2neff, -wh1neff*wh2neff,   +wh2neff,  wh2neff*(wlneff+wh2neff)];

% Transversal-Roll
matTR=wten*wnn/wlneff*...
     [ 1,      -wh1neff,       -1,      +wh2neff;...
     -wh1neff, -wh1neff*(wlneff-wh1neff), +wh1neff,   -wh1neff*wh2neff;...
     -1,       +wh1neff,        1,      -wh2neff;...
     +wh2neff, -wh1neff*wh2neff,    -wh2neff,  wh2neff*(wlneff+wh2neff)];

% Vertical
matV=wksn*wnn*(1+1i/wQsn)*[1  -1; -1  1];

% Yaw
matY=wktn*wnn*(1+1i/wQn)*[1  -1; -1  1];

% Combined matrix
matKwn([1,5,7,11],[1,5,7,11])=matKwn([1,5,7,11],[1,5,7,11])+matLP;
matKwn([2,4,8,10],[2,4,8,10])=matKwn([2,4,8,10],[2,4,8,10])+matTR;
matKwn([3,9],[3,9])=matKwn([3,9],[3,9])+matV;
matKwn([6,12],[6,12])=matKwn([6,12],[6,12])+matY;

end