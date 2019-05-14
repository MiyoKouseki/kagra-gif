%% Read parameters from SUMCON parameter file for simulink simulation
% written by A. Shoda

%% Material parameters
% Copied from SUMCON
% Should be implemented i = 9 section
% Young's modulus % Poisson ratio % Shear modulus % Volume density % Tensile strength % Quality factor
MatPara = {
    {184e9, 0.32, 184e9/2/(1+0.32), 8.0e3, 2.0e9, 1.0e4},; %Maraging Steel 
    {200e9, 0.28, 200e9/2/(1+0.28), 7.8e3, 2.0e9, 1.0e4},; %C-70 Steel
    {411e9, 0.28, 411e9/2/(1+0.28),19.3e3, 2.0e9, 1.0e4},; %Tungsten
    {134e9, 0.30, 134e9/2/(1+0.30), 8,4e3, 2.0e9, 2.0e5},; %Copper Berylium
    {345e9, 0.30, 345e9/2/(1+0.30), 4.0e3, 2.0e9, 5.0e6},; %Sapphire
    {157e9, 0.30, 157e9/2/(1+0.30), 7.6e3, 2.0e9, 1.0e3},; %Bolfur
        };


%% read sumcon file
%SUMCONdir = '../../SUMCON/save'

SUMCONfile = input('SUMCON file? > ');

%SUMCONfile = strcat(SUMCONdir,SUMCONfile);
param = textread(SUMCONfile,'%c');
param = transpose(param);

%% find parameters

N_param = strfind(param, 'save$');
End_param = strfind(param, 'calc$');

%% define body name
i = 1;
% Check
%%%% Now constructing...

% convert mathematica format to matlab format
tmp_param = param((N_param(i)+5):(N_param(i+1)-1));
tmp_param = strrep(tmp_param,'"','''');
tmp_param = strrep(tmp_param,'True','true');
tmp_param = strrep(tmp_param,'False','false');
tmp_param = strcat(tmp_param,';');
eval(tmp_param);    % bdn made

% Load rigid body
rigidbodyname = {};
        
for k = 1:length(bdn)
    if bdn{k}{1} == 0
        rigidbodyname = horzcat(rigidbodyname, bdn{k}{2});
    end
end

Nbody = length(rigidbodyname);

%% body position
i = 2;

%% passive damper
i = 3;

tmp_param = param((N_param(i)+5):(N_param(i+1)-1));
tmp_param = strrep(tmp_param,'"','''');
tmp_param = strrep(tmp_param,'*^','*10^');
tmp_param = strcat(tmp_param,';');
eval(tmp_param);

for i = 1:length(damp)
    % Load damper position
    body1 = rigidbodyname(damp{i}{2});
    body2 = rigidbodyname(damp{i}{3});
    
    % Damping point on body1
    pos1 = cell2mat(damp{i}{4});
    eq = strcat('pos_damp',body1,'=',mat2str(pos1),';');
    eval(char(eq));
    
    % Damping point on body2
    pos2 = cell2mat(damp{i}{5});
    eq = strcat('pos_damp',body2,'=',mat2str(pos2),';');
    eval(char(eq));
    
    % Damping coefficient matrix
    % Assume No Cross Coupling
    T = damp{i}{6}{1}{1};
    V = damp{i}{6}{2}{2};
    L = damp{i}{6}{3}{3};
    Roll = damp{i}{6}{4}{4};
    Yaw = damp{i}{6}{5}{5};
    Pitch = damp{i}{6}{6}{6};
    mat = [L,T,V,Pitch,Roll,Yaw];
    eq = strcat('mat_damp',body1,body2,'=',mat2str(pos2),';');
    eval(char(eq));
end

%% file name
i = 4;

%% HL ??
i = 5;

%% initial position
i = 6;

%% Inverted Pendulum
i = 7;

tmp_param = param((N_param(i)+5):(N_param(i+1)-1));
tmp_param = strrep(tmp_param,'True','true');
tmp_param = strrep(tmp_param,'False','false');
tmp_param = strrep(tmp_param,'"','''');
tmp_param = strrep(tmp_param,'*^','*10^');
tmp_param = strcat(tmp_param,';');
eval(tmp_param);

for i = 1:length(IP)
    N_ubody = IP{i}{1};
    N_lbody = IP{i}{2};
    if N_ubody == 1
        ubody = 'GND';
    else
        ubody = rigidbodyname(N_ubody-1);
    end
    lbody = rigidbodyname(N_lbody-1);
    
    % ip name
    ipname = strcat('ip',ubody,'2',lbody);
    
    % total load [kg]
    eq = strcat('m_',ipname,'=',num2str(IP{i}{10}),';');
    eval(char(eq));
    
    % Length of legs [m]
    eq = strcat('l_',ipname,'=',num2str(IP{i}{7}),';');
    eval(char(eq));
    
    % Distance between leg and center [m]
    pos_x = IP{i}{3}{1}{1};
    pos_y = IP{i}{3}{1}{2};
    dist = sqrt(pos_x^2 + pos_y^2);
    eq = strcat('r_',ipname,'=',num2str(dist),';');
    eval(char(eq));
    
    % Saturation level due to CoP
    db = IP{i}{8};
    eq = strcat('B_',ipname,'=',num2str(10^(db/20)),';');
    eval(char(eq));
    
    % Quality factor
    eq = strcat('Q_',ipname,'=',num2str(IP{i}{5}{4}),';'); % Quality facor of YAW
    eval(char(eq));
    
    % Additional torsion stiffness [Nm/rad]
    eq = strcat('kt_',ipname,'=',num2str(IP{i}{4}{4}),';');
    eval(char(eq));
end


%% Mass and MOI
i = 8;
tmp_param = param((N_param(i)+5):(N_param(i+1)-1));
tmp_param = strcat(tmp_param,';');
eval(tmp_param);

%mass
for i = 1:Nbody
    % Mass of the bodies
    mbodyname = strcat('m',rigidbodyname(i)); % name of parameters
    bodymass = mass{1+i}{1};
    eq = strcat(mbodyname,'=',num2str(bodymass),';');
    eval(char(eq));
    
    % MOI of the bodies
    moibodyname = strcat('moi',rigidbodyname(i)); % name of parameters
    bodymoi_x = cell2mat(mass{i+1}{2}{1});
    bodymoi_y = cell2mat(mass{i+1}{2}{2});
    bodymoi_z = cell2mat(mass{i+1}{2}{3});
    bodymoi = [bodymoi_x; bodymoi_y; bodymoi_z];
    bodymoi = circshift(bodymoi,1,2);   % convert the dimension
    bodymoi = circshift(bodymoi,1,1);
    eq = strcat(moibodyname,'=',mat2str(bodymoi),';');
    eval(char(eq));
end

%% material information
i = 9;

%% shape
i = 10;

%% vertical spring
i = 11;

tmp_param = param((N_param(i)+5):(N_param(i+1)-1));
tmp_param = strrep(tmp_param,'True','true');
tmp_param = strrep(tmp_param,'False','false');
tmp_param = strrep(tmp_param,'"','''');
tmp_param = strrep(tmp_param,'*^','*10^');
tmp_param = strcat(tmp_param,';');
eval(tmp_param);


%% wire
i = 12;

tmp_param = param((N_param(i)+5):(N_param(i+1)-1));
tmp_param = strrep(tmp_param,'"','''');
tmp_param = strrep(tmp_param,'*^','*10^');
tmp_param = strcat(tmp_param,';');
eval(tmp_param);

%% GAS Filter

for i = 1:length(vspr)
    % Load GAS position
    % Assume that GAS is at the upper body of the wire
    wireNum = vspr{i}{1};
    N_ubody = wire{wireNum}{1};
    N_lbody = wire{wireNum}{3};
    if N_ubody == 1
        ubody = 'GND';
    else
        ubody = rigidbodyname(N_ubody-1);
    end
    lbody = rigidbodyname(N_lbody-1);
    
    % Name of wire
    wirename = strcat('w',ubody,'2',lbody);
    
    % Isolation saturation level due to CoP
    db = vspr{i}{6};
    eq = strcat('Bsp_',wirename,'=',num2str(10^(db/20)),';');
    eval(char(eq));
    
    % Q of spring
    eq = strcat('Qsp_',wirename,'=',num2str(vspr{i}{9}),';');
    eval(char(eq));
    
    % Resonant frequency of vertical spring
    question = strcat('GAS resonant frequency at',ubody,' > ');
    Fr = input(question);
    eq = strcat('fsp_',wirename,'=',num2str(Fr),';');
    eval(char(eq));
    
end

%% wire2
i = 13;

tmp_param = param((N_param(i)+5):(End_param(1)-1));
tmp_param = strrep(tmp_param,'True','true');
tmp_param = strrep(tmp_param,'False','false');
tmp_param = strrep(tmp_param,'*^','*10^');
tmp_param = strcat(tmp_param,';');
eval(tmp_param);

for i = 1:length(wire2)
    % Load connections (ubody = upper body, lbody = lower body)
    N_ubody = wire2{i}{2};
    N_lbody = wire2{i}{3};
    if N_ubody == 1
        ubody = 'GND';
    else
        ubody = rigidbodyname(N_ubody-1);
    end
    lbody = rigidbodyname(N_lbody-1);
    
    
    % Name of wire
    wirename = strcat('w',ubody,'2',lbody);
    
    % Number of wire
    eq = strcat('n_',wirename,'=',num2str(wire2{i}{1}),';');
    eval(char(eq));
    
    % Wire length [m]
    eq = strcat('l_',wirename,'=',num2str(wire2{i}{6}{1}),';');
    eval(char(eq));
    
    % Wire diameter [m]
    eq = strcat('d_',wirename,'=',num2str(wire2{i}{6}{2}),';');
    eval(char(eq));
    
    % Total load on wires [kg]
    Load = wire2{i}{7}; % Load on each wire [N]
    Load = Load*wire2{i}{1}/9.8; % Total load on wires [kg]
    eq = strcat('m_',wirename,'=',num2str(Load),';');
    eval(char(eq));
    
    % Material
    % 1; Young's modulus % 2; Poisson ratio % 3; Shear modulus % 4; Volume density % 5; Tensile strength % 6; Quality factor
    MaterialNum = wire2{i}{5};
    eq = strcat('E_',wirename,'=',num2str(MatPara{MaterialNum}{1}),';');
    eval(char(eq));
    eq = strcat('G_',wirename,'=',num2str(MatPara{MaterialNum}{3}),';');
    eval(char(eq));
    eq = strcat('T_',wirename,'=',num2str(MatPara{MaterialNum}{5}),';');
    eval(char(eq));
    eq = strcat('Q_',wirename,'=',num2str(MatPara{MaterialNum}{6}),';');
    eval(char(eq));
    
    % wire position
    if wire2{i}{1} == 1
        % Vertical position of upper SP from upper body CoM [m]
        eq = strcat('h1_',wirename,'=',num2str(wire2{i}{4}{1}),';');
        eval(char(eq));
        % Vertical position of upper SP from upper body CoM [m]
        eq = strcat('h2_',wirename,'=',num2str(wire2{i}{4}{2}),';');
        eval(char(eq));
    elseif wire2{i}{1} == 3
        % Vertical position of upper SP from upper body CoM [m]
        eq = strcat('h1_',wirename,'=',num2str(wire2{i}{4}{1}),';');
        eval(char(eq));
        % Vertical position of upper SP from upper body CoM [m]
        eq = strcat('h2_',wirename,'=',num2str(wire2{i}{4}{2}),';');
        eval(char(eq));
        % Horizontal distance btw upper SP and upper body CoM [m]
        eq = strcat('r1_',wirename,'=',num2str(wire2{i}{4}{3}),';');
        eval(char(eq));
        % Horizontal distance btw lower SP and lower body CoM [m]
        eq = strcat('r2_',wirename,'=',num2str(wire2{i}{4}{3}),';'); %% Assume that the wires are pararell
        eval(char(eq));
    elseif wire2{i}{1} == 4
        % Vertical position of upper SP from upper body CoM [m]
        eq = strcat('h1_',wirename,'=',num2str(wire2{i}{4}{1}),';');
        eval(char(eq));
        % Vertical position of upper SP from upper body CoM [m]
        eq = strcat('h2_',wirename,'=',num2str(wire2{i}{4}{2}),';');
        eval(char(eq));
        % Transversal sepration of wires in upper SP
        eq = strcat('w1_',wirename,'=',num2str(wire2{i}{4}{3}),';');
        eval(char(eq));
        % Transversal sepration of wires in upper SP
        eq = strcat('w2_',wirename,'=',num2str(wire2{i}{4}{3}),';'); % Assume symmetry
        eval(char(eq));
        % Longitudinal separation of wires in upper SP
        eq = strcat('d1_',wirename,'=',num2str(wire2{i}{4}{4}),';');
        eval(char(eq));
        % Longitudinal separation of wires in upper SP
        eq = strcat('d2_',wirename,'=',num2str(wire2{i}{4}{4}),';');
        eval(char(eq));
    end
    
end
        
        
        
        
    % Vertical position of upper SP from upper body CoM [m]
    eq = strcat('h1_',wirename,'=',num2str(wire2{i}{4}{1}),';');
    eval(char(eq));
    % Vertical position of upper SP from upper body CoM [m]
    eq = strcat('h2_',wirename,'=',num2str(wire2{i}{4}{2}),';');
    eval(char(eq));
    
