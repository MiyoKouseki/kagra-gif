function matKwn=makematKwn2(wtn,wln,wh1n,wh2n,weffbn,ww1n,ww2n,wQn,wQsn,wksn,wktn)

% makematKwn1 calculates the stiffness matrix of a single wire suspension.
% Following arguments are required;
%   wtn: total load on wires [N]
%   wln:  wire length
%   wh1n: vertical position of upper suspension point from center of mass
%         of the upper body
%   wh2n: vertical position of lower suspension point from center of mass
%         of the lower body
%   ww1n: separation of upper suspension point and center of mass
%         in transversal direction
%   ww2n: separation of lower suspensoin point and center of mass
%         in transversal direction
%   wQn:  Quality factor of wire material
%   wQsn: Quality factor of bounce mode (spring mode)
%   wksn: Spring constant about bouce mode [N/m]
%   wksn: Spring constant about torsion mode [N*m/rad]

wnn = 2; % number of wires
matKwn=zeros(12,12);

wdwn = ww1n-ww2n;              % wire horizontal length
wh0n  = sqrt(wln^2-wdwn^2);    % wire vertical length
delta=weffbn*(1+1i/wQn/2);     % complex bending length
wh1neff=wh1n-delta*wh0n/wln;   % upper effective bending point
wh2neff=wh2n+delta*wh0n/wln;   % lower effective bending point
wlneff =wln-2*delta;           % effective wire length
% wh0neff=wh0n-2*delta*wh0n/wln; % effective vertical length
% ww1neff=ww1n-delta*wdwn/wln;   % effective upper SP position
% ww2neff=ww2n+delta+wdwn/wln;   % effective lower SP position
% wksnc=wksn*(1+1i/wQsn);        % complex spring constant

% Longitudinal-Pitch
matLP=wten*wnn/wlneff*...
    [ 1,      +wh1neff,       -1,      -wh2neff;...
    +wh1neff, -wh1neff*(wlneff-wh1neff), -wh1neff,   -wh1neff*wh2neff;...
    -1,       -wh1neff,        1,      +wh2neff;...
    -wh2neff, -wh1neff*wh2neff,   +wh2neff,  wh2neff*(wlneff+wh2neff)];

% Transversal-Roll
K_T1T1 =  wten*wnn/wlneff*(wh0neff/wlneff)^2 + wksn*wnn*(wdwn/wln)^2;
K_R1T1 = -wten*wnn/wlneff*wh0neff*(wh0neff*wh1neff+wdwneff*ww1neff)/wlneff^2 ...
         -wksn*wnn*wdwn*(wdwn*wh1n-wh0n*ww1n)/wln^2;
K_T2T1 = -K_T1T1;
K_R2T1 =  wten*wnn/wlneff*wh0neff*(wh0neff*wh2neff+wdwneff*ww2neff)/wlneff^2 ...
         +wksn*wnn*wdwn*(wdwn*wh2n-wh0n*ww2n)/wln^2;
K_T1R1 =  K_R1T1;
K_R1R1 =  wten*wnn

matTR=wten*wnn/wlneff*...
     [ 1,      -wh1neff,       -1,      +wh2neff;...
     -wh1neff, -wh1neff*(wlneff-wh1neff), +wh1neff,   -wh1neff*wh2neff;...
     -1,       +wh1neff,        1,      -wh2neff;...
     +wh2neff, -wh1neff*wh2neff,    -wh2neff,  wh2neff*(wlneff+wh2neff)]...
     +wksn*ww1n^2*wnn*(1+1i/wQsn)*...
     [0    0   0   0;...
      0    1   0  -1;...
      0    0   0   0;...
      0   -1   0   1];

% Vertical
matV=wksn*wnn*(1+1i/wQsn)*[1  -1; -1  1];

% Yaw
matY=wktn*wnn*(1+1i/wQn)*[1  -1; -1  1]+...
     wtn/wlneff*ww1n^2*[1  -1; -1  1];

% Combined matrix
matKwn([1,5,7,11],[1,5,7,11])=matKwn([1,5,7,11],[1,5,7,11])+matLP;
matKwn([2,4,8,10],[2,4,8,10])=matKwn([2,4,8,10],[2,4,8,10])+matTR;
matKwn([3,9],[3,9])=matKwn([3,9],[3,9])+matV;
matKwn([6,12],[6,12])=matKwn([6,12],[6,12])+matY;

end