
%% ABOUT THIS FILE
% ----------------------------------------------------------------------
% Type-___ SAS for KAGRA
% Coded by ___ on ___.
% ----------------------------------------------------------------------

%% PRELIMINARY ----------------------------------------------------------------------------
clear all;  % Clear workspace
close all;  % Close plot windows
addpath('./utility');  % Add path to utilities
g = 9.81;

%% IMPORT SUSPENSION MODEL ----------------------------------------------------------------------------
matfile='matlab';              % [load the matfile here]
load([matfile,'.mat']);

%% TUNING DAMPER
% This part compensates the failure in converting the structural damping to
% viscous damping.
% [we can discuss later about this topic.]

%% IMPORT SERVO FILTERS ----------------------------------------------------------------------------
%addpath('servofilter');         % Add path to servo
TypeA_paramNoCtrl180517;        % Damping MODE    % [load the mdlfile here]
%rmpath ('servofilter');         % Remove path to servo

%% IMPORT SIMULINK MODEL -------------------------------------------------------------
mdlfile='TypeA_siso180515';                 % [load the mdlfile here]
st     =linmod(mdlfile);
invl   =strrep(st.InputName, [mdlfile,'/'],'');
outvl  =strrep(st.OutputName,[mdlfile,'/'],'');
sysc   =ss(st.a,st.b,st.c,st.d,'inputname',invl,'outputname',outvl);


%% FREQUENCY ----------------------------------------------------------------------
freq=logspace(-2,2,1001);


%% TRANSFER FUNCTION ----------------------------------------------------------------------
%output_dir_OL = '~';
bodesusplot(sysc,'accGndL','LVDT_IPL',freq);
%bodesusplot(sysc,'noiseActIPL','LVDT_IPL',freq);
figname = sprintf('TF.pdf');
%export_fig(figname)