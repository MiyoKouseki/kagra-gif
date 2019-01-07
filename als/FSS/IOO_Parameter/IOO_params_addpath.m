function IOO_params_addpath
    parents = fileparts(mfilename('fullpath'));
    addpath([parents filesep 'IOO_params']);
    addpath([parents filesep 'IOO_params' filesep 'Actuator']);
    addpath([parents filesep 'IOO_params' filesep 'Actuator' filesep 'data']);
    addpath([parents filesep 'IOO_params' filesep 'Cavity']);
    addpath([parents filesep 'IOO_params' filesep 'Cavity' filesep 'data']);
    addpath([parents filesep 'IOO_params' filesep 'Common']);
    addpath([parents filesep 'IOO_params' filesep 'Servo']);
    addpath([parents filesep 'IOO_params' filesep 'Servo' filesep 'data']);