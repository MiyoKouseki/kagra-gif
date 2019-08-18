%% Read parameters from SUMCON parameter file for simulink simulation
% written by A. Shoda 2016.3.29
% modified by K. Okutomi 2016.6.20

%% Clear all

clear all;  % Clear workspace
close all;  % Close plot windows

addpath('../../utility');  % Add path to utilities
% addpath('sumconSaveFile');

%% Material parameters
% Copied from SUMCON
% Should be implemented i = 9 section
% Young's modulus % Poisson ratio % Shear modulus % Volume density % Tensile strength % Quality factor
matPara = {
    {184e9, 0.32, 184e9/2/(1+0.32), 8.0e3, 2.0e9, 1.0e4},; %Maraging Steel 
    {200e9, 0.28, 200e9/2/(1+0.28), 7.8e3, 2.0e9, 1.0e4},; %C-70 Steel
    {411e9, 0.28, 411e9/2/(1+0.28),19.3e3, 2.0e9, 1.0e4},; %Tungsten
    {134e9, 0.30, 134e9/2/(1+0.30), 8,4e3, 2.0e9, 2.0e5},; %Copper Berylium
    {345e9, 0.30, 345e9/2/(1+0.30), 4.0e3, 2.0e9, 5.0e6},; %Sapphire
    {157e9, 0.30, 157e9/2/(1+0.30), 7.6e3, 2.0e9, 1.0e3},; %Bolfur
        };


%% Read sumcon file

sumconFileName = input('SUMCON file? > ');

sumconSaveString = textread(sumconFileName,'%c');
sumconSaveString = transpose(sumconSaveString);

%% Convert mathematica format to matlab format
sumconSaveString = strrep(sumconSaveString,'"','''');
sumconSaveString = strrep(sumconSaveString,'True','true');
sumconSaveString = strrep(sumconSaveString,'False','false');
sumconSaveString = strrep(sumconSaveString,'*^','*10^');

%% Find parameters
clear SumconSaveIndex;

sumconParamIndex = regexp(sumconSaveString, 'save[$]\w*');
sumconParamIndex = horzcat(sumconParamIndex, min(strfind(sumconSaveString, 'calc$')));
sumconParamKey = regexp(sumconSaveString, 'save[$]\w*', 'match');
sumconParamKey = strrep(sumconParamKey, 'save$', '');
SumconSaveIndex = struct;
for j = 1:length(sumconParamKey)
    SumconSaveIndex.(sumconParamKey{j}) = [sumconParamIndex(j)+5 sumconParamIndex(j+1)-1];
end

%% sus model name
susmodelname = input('sus structure name ? > ');
sus = makesusstructure(susmodelname);

%% Define body name
tmp = SumconSaveIndex.bdn;
tmp_param = sumconSaveString(tmp(1):tmp(2));
tmp_param = strcat(tmp_param,';');
eval(tmp_param);    % bdn made

% Load rigid body
rigidbodyname = {};

for k = 1:length(bdn)
    if bdn{k}{1} == 0
        rigidbodyname = horzcat(rigidbodyname, bdn{k}{2});
        
    elseif bdn{k}{1} == 1
        groundname = bdn{k}{2};
        sus = addground(sus, groundname);
        fprintf('GND added \n');
    end
end

Nbody = length(rigidbodyname);

%% Body position

%% Damper
if isfield(SumconSaveIndex, 'damp')
    tmp = SumconSaveIndex.damp;
    tmp_param = sumconSaveString(tmp(1):tmp(2));
    tmp_param = strcat(tmp_param,';');
    eval(tmp_param);
end

%% Heat link

%% Inverted Pendulum
if isfield(SumconSaveIndex, 'IP')
    tmp = SumconSaveIndex.IP;
    tmp_param = sumconSaveString(tmp(1):tmp(2));
    tmp_param = strcat(tmp_param,';');
    eval(tmp_param);
end


%% Mass and MOI
tmp = SumconSaveIndex.mass;
tmp_param = sumconSaveString(tmp(1):tmp(2));
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
    
    sus = addrigidbody(sus,char(rigidbodyname(i)),bodymass,bodymoi);
end

%% Material information
tmp = SumconSaveIndex.mat;
tmp_param = sumconSaveString(tmp(1):tmp(2));
tmp_param = strcat(tmp_param,';');
% tmp_param = strrep(tmp_param,'mat','MatPara');
eval(tmp_param);
% MatPara = {{},;
%             };
% 

%% shape

%% Vertical spring
if isfield(SumconSaveIndex, 'vspr')
    tmp = SumconSaveIndex.vspr;
    tmp_param = sumconSaveString(tmp(1):tmp(2));
    tmp_param = strcat(tmp_param,';');
    eval(tmp_param);
end

%% wire
tmp = SumconSaveIndex.wire;
tmp_param = sumconSaveString(tmp(1):tmp(2));
tmp_param = strcat(tmp_param,';');
eval(tmp_param);

%% GAS Filter
if isfield(SumconSaveIndex, 'vspr')
    GASinfo = cell([length(vspr),1]);
    for i = 1:length(vspr)
        % Load GAS position
        % Assume that GAS is at the upper body of the wire
        wireNum = vspr{i}{1};
        N_ubody = wire{wireNum}{1};
        N_lbody = wire{wireNum}{3};
        if N_ubody == 1
            ubody = groundname;
        else
            ubody = rigidbodyname(N_ubody-1);
        end
        lbody = rigidbodyname(N_lbody-1);

        % Name of wire
        wirename = strcat('w',ubody,'2',lbody);

        % Isolation saturation level due to CoP
        db = vspr{i}{6};
        Bsp = 10^(db/20);
        eq = strcat('Bsp_',wirename,'=',num2str(Bsp),';');
        eval(char(eq));

        % Q of spring
        Qsp = vspr{i}{9};
        eq = strcat('Qsp_',wirename,'=',num2str(vspr{i}{9}),';');
        eval(char(eq));

        % Resonant frequency of vertical spring
        question = strcat('GAS resonant frequency at',ubody,' > ');
        Fr = input(char(question));
        eq = strcat('fsp_',wirename,'=',num2str(Fr),';');
        eval(char(eq));

        GASinfo{i} = {N_ubody,N_lbody,Bsp,Qsp,Fr};

    end
end

%% wire2
tmp = SumconSaveIndex.wire2;
tmp_param = sumconSaveString(tmp(1):tmp(2));
tmp_param = strcat(tmp_param,';');
eval(tmp_param);


for i = 1:length(wire2)
    % Load connections (ubody = upper body, lbody = lower body)
    N_ubody = wire2{i}{2};
    N_lbody = wire2{i}{3};
    if N_ubody == 1
        ubody = groundname;
    else
        ubody = rigidbodyname(N_ubody-1);
    end
    lbody = rigidbodyname(N_lbody-1);
    
    
    % Name of wire
    wirename = strcat('w',ubody,'2',lbody);
    
    % Number of wire
    n = wire2{i}{1};
    eq = strcat('n_',wirename,'=',num2str(n),';');
    eval(char(eq));
    
    % Wire length [m]
    l = wire2{i}{6}{1};
    eq = strcat('l_',wirename,'=',num2str(l),';');
    eval(char(eq));
    
    % Wire diameter [m]
    d = wire2{i}{6}{2};
    eq = strcat('d_',wirename,'=',num2str(d),';');
    eval(char(eq));
    
    % Total load on wires [kg]
    m = wire2{i}{7}; % Load on each wire [N]
    m = m*wire2{i}{1}/9.8; % Total load on wires [kg]
    eq = strcat('m_',wirename,'=',num2str(m),';');
    eval(char(eq));
    
    % Material
    % 1; Young's modulus % 2; Poisson ratio % 3; Shear modulus % 4; Volume density % 5; Tensile strength % 6; Quality factor
    MaterialNum = wire2{i}{5};
    E = matPara{MaterialNum}{1};
    eq = strcat('E_',wirename,'=',num2str(E),';');
    eval(char(eq));
    G = matPara{MaterialNum}{3};
    eq = strcat('G_',wirename,'=',num2str(G),';');
    eval(char(eq));
    T = matPara{MaterialNum}{5};
    eq = strcat('T_',wirename,'=',num2str(T),';');
    eval(char(eq));
    Q = matPara{MaterialNum}{6};
    eq = strcat('Q_',wirename,'=',num2str(Q),';');
    eval(char(eq));
    
    % wire position
    if n == 1
        % Vertical position of upper SP from upper body CoM [m]
        h1 = wire2{i}{4}{1};
        eq = strcat('h1_',wirename,'=',num2str(h1),';');
        eval(char(eq));
        % Vertical position of lower SP from lower body CoM [m]
        h2 = wire2{i}{4}{2};
        eq = strcat('h2_',wirename,'=',num2str(h2),';');
        eval(char(eq));
        
        %GASinfo{i} = {N_ubody,N_lbody,Bsp,Qsp,Fr};
        % Do you have GAS filter?
        GASproperty = 0;
        if isfield(SumconSaveIndex, 'vspr')
            for k = 1:length(GASinfo)
                if N_ubody == GASinfo{k}{1} && N_lbody == GASinfo{k}{2}
                    GASproperty = k;
                    break
                end
            end
        end
        %{N_ubody,N_lbody,ln,dn}
        
        % Do you have nailhead?
        if wire2{i}{6}{5} == 1
            NeckProperty = 1;
            ln = wire2{i}{6}{3};
            dn = wire2{i}{6}{4};
        else
            NeckProperty = 0;
        end
        
        
        if GASproperty ~= 0
            if NeckProperty == 1
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
               % Add suspension wires and springs
                sus = addsuswire(sus,...       % F0-F1
                    n,...               % number of wires
                    {...                       % OPTION
                    'spring',...               % add spring
                    'neck',...                 % wire with necks
                    },...                      %
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2...               % vertical position of lower SP
                    ],...                      %
                    [l,ln],...   % length & neck length
                    [d,dn],...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q,...               % Q factor
                    {'spring',...              % SPRING
                    GASinfo{GASproperty}{5},...             % resonant frequency
                    GASinfo{GASproperty}{3},...             % saturation due to CoP
                    GASinfo{GASproperty}{4}...              % spring Q
                    }...                       %
                    );
            else
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'spring'
                    },...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    ],...                      %
                    l,...                   % length & neck length
                    d,...                   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    {'spring',...              % SPRING
                    GASinfo{GASproperty}{5},...             % resonant frequency
                    GASinfo{GASproperty}{3},...             % saturation due to CoP
                    GASinfo{GASproperty}{4}...              % spring Q
                    }...
                    );
            end
        else
            if NeckProperty == 1
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
               % Add suspension wires and springs
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'neck'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    ],...                      %
                    [l,ln],...               % length
                    [d,dn],...               % diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    );
            else
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    ],...                      %
                    l,...               % length
                    d,...               % diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    );
            end
        end
        
    elseif n == 3
        % Vertical position of upper SP from upper body CoM [m]
        h1 = wire2{i}{4}{1};
        eq = strcat('h1_',wirename,'=',num2str(h1),';');
        eval(char(eq));
        % Vertical position of upper SP from upper body CoM [m]
        h2 = wire2{i}{4}{2};
        eq = strcat('h2_',wirename,'=',num2str(h2),';');
        eval(char(eq));
        % Horizontal distance btw upper SP and upper body CoM [m]
        r1 = wire2{i}{4}{3};
        eq = strcat('r1_',wirename,'=',num2str(r1),';');
        eval(char(eq));
        % Horizontal distance btw lower SP and lower body CoM [m]
        r2 = wire2{i}{4}{3};
        eq = strcat('r2_',wirename,'=',num2str(r2),';'); %% Assume that the wires are pararell
        eval(char(eq));
        
        % Do you have GAS filter?
        GASproperty = 0;
        for k = 1:length(GASinfo)
            if N_ubody == GASinfo{k}{1} && N_lbody == GASinfo{k}{2}
                GASproperty = k;
                break
            end
        end
        %{N_ubody,N_lbody,ln,dn}
        % Do you have nailhead?
        if wire2{i}{6}{5} == 1
            NeckProperty = 1;
            ln = wire2{i}{6}{3};
            dn = wire2{i}{6}{4};
        else
            NeckProperty = 0;
        end
        
        if GASproperty ~= 0
            if NeckProperty == 1
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'spring', 'neck'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    r1...               % horizontal distance of upper SP from CoM
                    ],...                      %
                    [l,ln],...   % length & neck length
                    [d,dn],...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q,...                % Q factor
                    {'spring',...              % SPRING
                    GASinfo{GASproperty}{5},...             % resonant frequency
                    GASinfo{GASproperty}{3},...             % saturation due to CoP
                    GASinfo{GASproperty}{4}...              % spring Q
                    }...
                    );
            else
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'spring'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    r1...               % horizontal distance of upper SP from CoM
                    ],...                      %
                    l,...                 % length
                    d,...               % diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q,...                % Q factor
                    {'spring',...              % SPRING
                    GASinfo{GASproperty}{5},...             % resonant frequency
                    GASinfo{GASproperty}{3},...             % saturation due to CoP
                    GASinfo{GASproperty}{4}...              % spring Q
                    }...
                    );
            end 
 
        else
            if NeckProperty == 1
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'neck'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    r1...               % horizontal distance of upper SP from CoM
                    ],...                      %
                    [l,ln],...   % length & neck length
                    [d,dn],...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    );
            else
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    r1...               % horizontal distance of upper SP from CoM
                    ],...                      %
                    l,...                 % length
                    d,...               % diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    );
            end
        end

    elseif wire2{i}{1} == 4
        % Vertical position of upper SP from upper body CoM [m]
        h1 = wire2{i}{4}{1};
        eq = strcat('h1_',wirename,'=',num2str(h1),';');
        eval(char(eq));
        % Vertical position of upper SP from upper body CoM [m]
        h2 = wire2{i}{4}{2};
        eq = strcat('h2_',wirename,'=',num2str(h2),';');
        eval(char(eq));
        % Transversal sepration of wires in upper SP
        w1 = wire2{i}{4}{3};
        eq = strcat('w1_',wirename,'=',num2str(w1),';');
        eval(char(eq));
        % Transversal sepration of wires in upper SP
        w2 = wire2{i}{4}{3};
        eq = strcat('w2_',wirename,'=',num2str(w2),';'); % Assume symmetry
        eval(char(eq));
        % Longitudinal separation of wires in upper SP
        d1 = wire2{i}{4}{4};
        eq = strcat('d1_',wirename,'=',num2str(d1),';');
        eval(char(eq));
        % Longitudinal separation of wires in upper SP
        d2 = wire2{i}{4}{4};
        eq = strcat('d2_',wirename,'=',num2str(d2),';');
        eval(char(eq));
        
        %GASinfo{i} = {N_ubody,N_lbody,Bsp,Qsp,Fr};
        % Do you have GAS filter?
        GASproperty = 0;
        for k = 1:length(GASinfo)
            if N_ubody == GASinfo{k}{1} && N_lbody == GASinfo{k}{2}
                GASproperty = k;
                break
            end
        end
        %{N_ubody,N_lbody,ln,dn}
        % Do you have nailhead?
        if wire2{i}{6}{5} == 1
            NeckProperty = 1;
            ln = wire2{i}{6}{3};
            dn = wire2{i}{6}{4};
        else
            NeckProperty = 0;
        end
        
        if GASproperty ~= 0
            if NeckProperty == 1
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'spring', 'neck'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    w1,...              % transversal position of upper SP
                    d1,...              % longitudinal position of upper SP
                    ],...                      %
                    [l,ln],...   % length & neck length
                    [d,dn],...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    {'spring',...              % SPRING
                    GASinfo{GASproperty}{5},...             % resonant frequency
                    GASinfo{GASproperty}{3},...             % saturation due to CoP
                    GASinfo{GASproperty}{4}...              % spring Q
                    }...
                    );
            else
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'spring'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    w1,...              % transversal position of upper SP
                    d1,...              % longitudinal position of upper SP
                    ],...                      %
                    l,...   % length & neck length
                    d,...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    {'spring',...              % SPRING
                    GASinfo{GASproperty}{5},...             % resonant frequency
                    GASinfo{GASproperty}{3},...             % saturation due to CoP
                    GASinfo{GASproperty}{4}...              % spring Q
                    }...
                    );
            end
        else
            if NeckProperty == 1
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {'neck'},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    w1,...              % transversal position of upper SP
                    d1,...              % longitudinal position of upper SP
                    ],...                      %
                    [l,ln],...   % length & neck length
                    [d,dn],...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    );
            else
                fprintf('wire btw %s and %s , GAS = %f, Neck = %f \n', char(ubody), char(lbody), GASproperty, NeckProperty);
                sus = addsuswire(sus,...       % F0-MD
                    n,...               % number of wires
                    {},...                     % OPTION
                    char(ubody),...                   % upper body
                    char(lbody),...                   % lower body
                    [...                       % GEOMETRIC PARAMETER
                    h1,...              % vertical position of upper SP
                    h2,...              % vertical position of lower SP
                    w1,...              % transversal position of upper SP
                    d1,...              % longitudinal position of upper SP
                    ],...                      %
                    l,...   % length & neck length
                    d,...   % diameter & neck diameter
                    m,...               % total load
                    E,...               % Young's modulus
                    G,...               % shear modulus
                    Q...                % Q factor
                    );
            end
        end
    else
        warning('Sorry, I cannot add wire...');
        return
    end
    
end
 

%% Add Damper
if isfield(SumconSaveIndex, 'damp')
    for i = 1:length(damp)
        % Load damper position
        body1 = bdn{damp{i}{2}}(2);
        body2 = bdn{damp{i}{3}}(2);

        % Damping point on body1
        pos1 = cell2mat(damp{i}{4});
        pos1 = circshift(pos1,1,2);  % convert the dimension
        pos1 = circshift(pos1,1,1);
        eq = strcat('pos_damp',body1,'=',mat2str(pos1),';');
        eval(char(eq));

        % Damping point on body2
        pos2 = cell2mat(damp{i}{5});
        pos2 = circshift(pos2,1,2);  % convert the dimension
        pos2 = circshift(pos2,1,1);
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
        mat = diag([L,T,V,Pitch,Roll,Yaw]);
        eq = strcat('mat_damp',body1,body2,'=',mat2str(mat),';');
        eval(char(eq));

        % Add damper
        sus = adddamper(sus,...        % MD-F1
            char(body1),...                   % body1
            char(body2),...                   % body2
            pos1,...             % damping point at body1
            pos2,...             % damping point at body2
            mat...            % damping matrix
            );
    end
end

%% Add IP
if isfield(SumconSaveIndex, 'IP')
    IPlbody = {};
    for i = 1:length(IP)
        N_ubody = IP{i}{1};
        N_lbody = IP{i}{2};
        if N_ubody == 1
            ubody = groundname;
        else
            ubody = rigidbodyname(N_ubody-1);
        end
        lbody = rigidbodyname(N_lbody-1);
        IPlbody = horzcat(IPlbody, lbody);
        % ip name
        ipname = strcat('ip',ubody,'2',lbody);

        % total load [kg]
        m = IP{i}{10};
        eq = strcat('m_',ipname,'=',num2str(m),';');
        eval(char(eq));

        % Length of legs [m]
        l = IP{i}{7};
        eq = strcat('l_',ipname,'=',num2str(l),';');
        eval(char(eq));

        % Distance between leg and center [m]
        pos_x = IP{i}{3}{1}{1};
        pos_y = IP{i}{3}{1}{2};
        r = sqrt(pos_x^2 + pos_y^2);
        eq = strcat('r_',ipname,'=',num2str(r),';');
        eval(char(eq));

        % Saturation level due to CoP
        db = IP{i}{8};
        B = 10^(db/20);
        eq = strcat('B_',ipname,'=',num2str(B),';');
        eval(char(eq));

        % Quality factor
        Q = IP{i}{5}{4};
        eq = strcat('Q_',ipname,'=',num2str(Q),';'); % Quality facor of YAW
        eval(char(eq));

        % Additional torsion stiffness [Nm/rad]
        kt = IP{i}{4}{4};
        eq = strcat('kt_',ipname,'=',num2str(kt),';');
        eval(char(eq));

        f = input('IP resonant frequency [Hz] ? >' );
        eq = strcat('f_',ipname,'=',num2str(f),';');
        eval(char(eq));
        %kt=80;
        % Add inverted pendulum
        sus = addinvpend(sus,...       % GND-F0
            char(ubody),...                  % base body
            char(lbody),...                   % supported body
            m,...             % total load [kg]
            r,...             % horizontal distance of leg from CoM [m]
            l,...             % leg length [m]
            f,...             % resonant frequency [Hz]
            Q,...             % quality factor of flexure
            B,...             % saturation level
            kt...             % additional torsion tiffness [Nm/rad]
            );

    end
end

%% Build suspension model

sus = buildsusmodel(sus);      % make state-space matrix


%% Simulink model

% input variables
var_a_GND = {strcat('accL',groundname),strcat('accT',groundname),strcat('accV',groundname),strcat('accR',groundname),strcat('accP',groundname),strcat('accY',groundname)}; % GND acceleration
invsim = [var_a_GND];
for body = rigidbodyname
    body = char(body);
    var = {strcat('actL',body),strcat('actT',body),strcat('actV',body),strcat('actR',body),strcat('actP',body),strcat('actY',body)};
    invsim = [invsim, var];
end

%% output variables

var_d_GND = {strcat('L',groundname),strcat('T',groundname),strcat('V',groundname),strcat('R',groundname),strcat('P',groundname),strcat('Y',groundname)}; % GND acceleration
var_v_GND = {strcat('velR',groundname),strcat('velP',groundname)};                       % GND velocity
outvsim = [var_d_GND];
outvsim = [outvsim, var_v_GND];
for body = rigidbodyname
    body = char(body);
    var_d = {strcat('L',body),strcat('T',body),strcat('V',body),strcat('R',body),strcat('P',body),strcat('Y',body)};
    outvsim = [outvsim, var_d];
    if isfield(SumconSaveIndex, 'IP')
        if cell2mat(strfind(IPlbody,body)) ~= zeros(size(IPlbody))
            var_v = {strcat('velL',body),strcat('velT',body),strcat('velV',body),strcat('velR',body),strcat('velP',body),strcat('velY',body)};
            outvsim = [outvsim, var_v];
        end
    end
end

%%
sys1=sus.ss;               % ss model
constructsimmodel(...      % CONSTRUCT SIMUKINK BLOCK MODEL
    susmodelname,...        % model name
    sys1,...               % state-space model
    'sys1',...             % state-space model name
    invsim,...             % input variables
    outvsim...             % output variables
    );                     % 
simulinkfile = strcat(susmodelname,'mdl');
save(simulinkfile,'sys1','sus');  % save sus model

%% Passive Calculation
%freq=logspace(-2,2,1001);
%bodesusplot(sys1,'actLF0','LF0',freq);

%% Eigen
eiglist=makeeigenlist(sus);