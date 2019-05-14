
%% ABOUT THIS FILE
% ----------------------------------------------------------------------
% Parmeter setting for NO CONTROL MODE
% Type-Bp for KAGRA
% Coded by Y.Fujii on 2016/11/16
% ----------------------------------------------------------------------

%% CONSTANTS
pp=2*pi;

%% ACTUATOR NORMALIZATION
% Normalize the actuators using local sensors at 0 Hz

% F2 (Normalized with LVDT signals)
gain_act_LBF = 32.9296747504;
gain_act_TBF = 32.9154009359;
gain_act_VBF = 30.303030303;
gain_act_PBF = 8.64557055148;
gain_act_RBF = 8.64557055148;
gain_act_YBF = 1.63692651118;

% IM (Normalized with OSEM signals)
gain_act_LIM = 14.4730076835;
gain_act_TIM = 14.4745237388;
gain_act_VIM = 19.4037631453;
gain_act_RIM = 1.56632872419;
gain_act_PIM = 1.56040613295;
gain_act_YIM = 0.6169784052;

% TM (Normalized with Oplev)
gain_act_LTM = 169.1045;
gain_act_PTM = 1.2097;
gain_act_YTM = 2.6742;

% GAS (Normalzed with LVDT signals)
gain_act_VF1 = 30.303030303;
gain_act_VF2 = 19.4037631453;

%% OpLev Coupling

Sens_Mat_OL = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    0,0,0,0,1,0; ...
    0,0,0,0,0,1];

%% ACTUATOR COUPLING MATRIX
%(L, T, V, R, P, Y) 

% BF actuator position shift:
%dv_BF = 0.022;
%dv_BR = -0.103;
%dv_BF = -0.005;
%dv_BR = -0.0;
dv_BF = 0.0;
dv_BR = 0.0;

Act_Mat_BR = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    dv_BR,0,0,0,1,0; ...
    0,0,0,0,0,1];
Act_Mat_BF = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    dv_BF,0,0,0,1,0; ...
    0,0,0,0,0,1];
Act_Mat_IR = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    0,0,0,0,1,0; ...
    0,0,0,0,0,1];
Act_Mat_IM = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    0,0,0,0,1,0; ...
    0,0,0,0,0,1];
Act_Mat_RM = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    0,0,0,0,1,0; ...
    0,0,0,0,0,1];
Act_Mat_TM = [...
    1,0,0,0,0,0; ...
    0,1,0,0,0,0; ...
    0,0,1,0,0,0; ...
    0,0,0,1,0,0; ...
    0,0,0,0,1,0; ...
    0,0,0,0,0,1];

%% BLENDING FILTERS
% This part constructs filters for blending LVDT and geophone signals.
% Blending filters are constructed from polynominal expression of a Laplace
% transformed equation (s+w0)^n, where w0 is the blending frequency and n
% is an arbitrary (odd) integer.
% 
% % BLENDING FREQUENCY: 0.3 Hz
% f_blend = 0.5;
% w_blend = f_blend*pp;
% 
% % COEFFICIENTS LIST OF POLYNOMINAL EXPRESSION OF (s+w0)^n
% n_blend = 7; % 5th order blending
% nbd = (n_blend+1)/2;
% cf_poly = zeros(1,n_blend+1);
% for n=0:n_blend; cf_poly(n+1)=nchoosek(n_blend,n)*w_blend^(n); end
% 
% % BLENDING FILTERS
% blend_HP = tf([cf_poly(1:nbd),zeros(1,nbd)],cf_poly);
% blend_LP = tf(cf_poly(nbd+1:n_blend+1),cf_poly);
% 
% % BLENDING FILTERS (ZPK EXPRESSION)
% % blend_LP = myzpk([0.075+1i*0.0581;0.075-1i*0.0581],[0.3;0.3;0.3;0.3;0.3],66.97);
% % blend_HP = myzpk([0.75+1i*0.581;0.75-1i*0.581;0;0;0],[0.3;0.3;0.3;0.3;0.3],1);
% 
% % GEOPHONE RESPONSES
% georesp  = zpk([-2.13+1i*5.19;-2.13-1i*5.19],[0;0],1);
% vel2disp = zpk([],0,1);
% 
% % BLENDING FILTERS WITH GEOPHONE RESPONSES
% % blend_LVDT = blend_LP;
% % blend_GEO  = minreal(blend_HP*georesp*vel2disp);
% blend_LVDT = 1;
% blend_GEO  = 0;

% PLOT 1
% freq1=logspace(-3,2,1001);
% mybodeplot({blend_LP,blend_HP,blend_LP+blend_HP},freq1);

% PLOT 2
% freq1=logspace(-3,2,1001);
% mybodeplot({blend_LVDT,blend_GEO},freq1);

%% SERVO FILTER
% GENERAL SERVO
% damping servo with 300 Hz cutoff
dampflt = myzpk(0,[3e1,3e1],9e2*pp);
dampflt1 = myzpk(0,[1e1,1e1],9e2*pp);
dampflt2 = myzpk([0,0.5,0.5],[3e2,3e2,30,30],9e7*pp);
dampflt4 = myzpk(0,[3e2,3e2],9e4*pp);
dampflt5 = myzpk(0,[1.5e2,1.5e2],50e3*pp);
% DC + damping servo with G=400 at 0.1 mHz
%dcdampflt = myzpk([1e-1;1e-1],[1e-4;1e1],10)...
%          * myzpk([],[3;3],(3*pp)^2);
% DC filter
dcflt = myzpk([],[1e-4;1e1],100*1e-3*pp^2)...
          * myzpk([],[3e-1;3e-1],(3e-1*pp)^2);
      
% % SERVO FILTER F0
% servo_LF0 = dcdampflt;
% servo_TF0 = dcdampflt;
% servo_YF0 = dcdampflt;

% SERVO FILTER F2
servo_LBF = 50.*dampflt;
servo_TBF = 50.*dampflt;
servo_VBF = 50.*dampflt;
servo_RBF = dampflt;
servo_PBF = dampflt;
servo_YBF = 15.*dampflt;


% SERVO FILTER IM
servo_LIM = 5.5*dampflt;
servo_TIM = 3.5*dampflt;
servo_VIM = 8.0*dampflt4;
servo_RIM = 8.0*dampflt5;
servo_PIM = 5.0*dampflt5;
servo_YIM = 5.0*dampflt5;

% SERVO FILTER TM
%servo_LTM = 0;
%servo_PTM = 0;
%servo_YTM = 0;

% SERVO FILTER GAS
% servo_VF0 = dcdampflt;
servo_VF1 = 0.2*dcflt;
servo_VF2 = 0.2*dcflt;

% SERVO FILTER OpLev
servo_oplev_PIM = 3*dampflt2;
servo_oplev_YIM = 0;
servo_oplev_LTM = dampflt;
servo_oplev_PTM = 10*dampflt;
servo_oplev_YTM = 5*dampflt;

% SERVO FILTER IFO
% servo_global_LF0 = 0;
servo_global_LIM = 0;
servo_global_LTM = 25*dampflt;

%% GAIN
gain_LBF = 0; gain_TBF = 0; gain_VBF = 0;
gain_PBF = 0; gain_RBF = 0; gain_YBF = 0;
gain_LIM = 0; gain_TIM = 0; gain_VIM = 0;
gain_RIM = 0; gain_PIM = 0; gain_YIM = 0;
%gain_LTM =  0; gain_PTM =  0; gain_YTM =  0;
gain_VF0 = 0; gain_VF1 = 0; gain_VF2 = 0;
gain_oplev_PIM = 0; gain_oplev_YIM = 0;
gain_oplev_LTM = 0; gain_oplev_PTM = 0; gain_oplev_YTM = 0;
gain_global_LF0 = 0; gain_global_LIM = 0; gain_global_LTM = 0;

% Saving point on 2016.11.16

