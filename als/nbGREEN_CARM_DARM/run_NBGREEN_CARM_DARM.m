% Noise budget  PLL test script
% Originally made by S. Kambara, largely modified by Y. Enomoto in 2018 
% modified K.Miyo from 2019/01/07

%% Add paths
clear all
close all
addpath('../');
findNbSVNroot;
addpath(genpath([NbSVNroot 'Common/Utils']));
addpath(genpath([NbSVNroot 'Dev/Utils/']));
cd([NbSVNroot,'nbGREEN_CARM_DARM']);

%% What to plot

plot_TFs = 1;
plot_NBs = 1;
plot_Saturations = 0;


%% Select servo topology

use_AOM = 1; % use AOM as a freq actuator of green, or use VCO option of PLL LO instead?

asym = 0.1; % asymmetry between X and Y green lock

use_X_as_CARM = 0;

%% Define some filters 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%PLL%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Changing_unit = zpk([],[0],2*pi);
Sen = 1;
%Filt_Temp = 0;
Filt_PZT = zpk([-2*pi*5e3,-2*pi*5e3],[0,0],0.01)*1;
Filt_PZT = myzpk('zpk',[],[100e3],.01)*myzpk('zpk',[10],[0],10) * myzpk('zpk',[2e3],[20],100)* myzpk('zpk',[2e3],[20],100);
%Act_Temp = 0
Act_PZT =  2e6;

%Gol = Sen*Filt_Temp*Act_Temp+Sen*Filt_PZT*Act_PZT;
Gol_PLL = Changing_unit*Sen*Filt_PZT*Act_PZT;

% Sensing Matrix and Actuator Matrix for CARM/DARM
Sensing = [1/2,1/2;1,-1];
if use_X_as_CARM
    Sensing = [1,0;0,-1];
end
Actuator = [1,1/2;1,-1/2];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%PDH%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Dictionaries
Filt = containers.Map;  % digital filter transfer functions [cnts/cnts]
Susp = containers.Map;  % suspension actuation transfer functions [m/N]
Noise = containers.Map; % all sorts of noises
PdResp = containers.Map;    % PD rensponse [A/W]
TransImp = containers.Map;  % PD trans impedance [V/A]
Elec = containers.Map;  % electronics gain [V/V]
Coil = containers.Map;  % coil gain [N/V]

CMS_Elec_CARM = containers.Map;


%%%%%%%parameter%%%%%%%%%
c = 299792458;
L = 3000;
%Finesse = 10;
lambda = 1.064e-6;
m2Hz = 2/lambda * c/2/L;
%%%%%%%%%%%%%%%%%%%%%%%%%
%freq = logspace(-3,6,100000);
freq = logspace(-3,6,1000);

%%
%%%%%%%Load IMC parameters%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% copied from FSS noise budget
addpath(genpath([NbSVNroot '/FSS']));
addpath(genpath([NbSVNroot '/FSS/IOO_Parameter']));
addpath(genpath([NbSVNroot '/FSS/functions']));
IOO_params_addpath();
load('IOO_params.mat');
[TTFSS_Gain,FB_SW_TTFSS,CMS_SW_IMC,FB_SW_MCL,CMS_SW_CARM,FB_SW_CARM,CavOpgain,SW] = ...
set_IOONB_config(...
    ...TTFSS
    'CG',              26,...
    'FG',              30,...
    'Fast_Sign',       -1,...
    'TEMPGAIN',         0,...
    ...
    ...IMC
    'IN1EN_IMC',          1,...
    'IN2EN_IMC',          1,...
    'IN2POL_IMC',          -1,...
    'IN1GAIN_IMC',     -20,...
    'K1IMC_MCL_GAIN',  0.1,...
    'SLOWPOL_IMC',       -1,...
    'COMCOMP_IMC',        1,...
    'SLOWBST_IMC',        1,...
    'K1IMC_MCL_FBSW',[1 2 10],...
    ...
    ...Opgain
'Opgain_RefCav',Cav('LPF_RefCav_1124'),...
    'Opgain_IMC',-Cav('LPF_IMC_1124'),...
    ...
    ...LOOP SW
    'LOOP_SW',ones(1,8)...
    );

change_filter = 1;



Filt_MCL = myzpk('zpk',[],[],.4);


%%

P_eff = 10e-3; % Effective power of green that enters a reflection PD
beta = 0.05; % mod index of green


T_ITM = 0.06+0.005;
R_ITM = 1-T_ITM;
T_ETM = 0.06;
R_ETM = 1-T_ETM;
Finesse = pi*sqrt(sqrt(R_ITM*R_ETM)) / (1-sqrt(R_ITM*R_ETM));

Cavity_Pole = zpk([],[-2*pi*c/4/L/Finesse],2*pi*c/4/L/Finesse);
%IMC_Cavity_Pole = myzpk('zpk',[],[6.0e3],1);
%IMC_Cavity_Pole = 1;
CARM_Cavity_Pole = myzpk('zpk',[],[0.8],1);
Sen_1 = Finesse/(c/2/L);
%Sen_2 = 1/m2Hz;
Sen_2 = 1;

green_PDH = P_eff * beta * T_ITM*sqrt(R_ETM)/(1-sqrt(R_ITM*R_ETM))^2 * 4*pi*L/c; % W/Hz
TransImp('green') = 0.3 * 100; % A/W * V/A  Rough number. TO BE CHECKED
DeModGain = 10.9; % Demodulation gain (see LIGO-F1100004-v4)

% CARM servo settings
Filt_sum = myzpk('zpk',[],[10],500);

CMS_SW_CARM('COMCOMP') = 1;
CMS_SW_CARM('COMBST') = 1; % # of common boost engaged
CMS_SW_CARM('IN2GAIN') = 30; % dB
CMS_SW_CARM('IN2EN') = 1;
CMS_SW_CARM('IN2POL') = -1;
CMS_SW_CARM('COMOPT') = 0;
CMS_SW_CARM('COMGEN') = 0;
CMS_SW_CARM('FASTEN') = 1;
CMS_SW_CARM('FASTPOL') = 1;
CMS_SW_CARM('FASTOPT') = 0;
CMS_SW_CARM('FASTGAIN') = -20; % dB

CMS_SW_CARM('SLOWPOL') = -1;
CMS_SW_CARM('SLOWBST') = 0;
CMS_SW_CARM('SLOWCOMP') = 1; % Disabled if 1
CMS_SW_CARM('SLOWGEN') = 0;
CMS_SW_CARM('SLOWBY') = 0;
CMS_SW_CARM('SLOWOPT') = 0;

CMS_Elec_CARM = CMS_Elec;

CMS_Elec_CARM('common_comp') = myzpk('zpk',[4e3],[40],100);
CMS_Elec_CARM('common_bst1') = myzpk('zpk',[1000],[10],100);
CMS_Elec_CARM('common_bst2') = myzpk('zpk',[1000],[10],100);

%CMS_Elec_CARM('FitStage_AOM') = 1;
%CMS_Elec_CARM('common_bst3') = myzpk('zpk',[1000],[10],1);


% DARM servo settings
Filt_darm = myzpk('zpk',[30],[300],3e4);
if use_X_as_CARM
    Filt_darm = myzpk('zpk',[30],[300],3e4)*myzpk('zpk',[10],[1],10);
end
%Filt_darm = myzpk('zpk',[10],[100],1)*myzpk('zpk',[.3],[3],.10);


% RF
Filt_GR1 = myzpk('zpk',[400],[40;100e3],.1)*myzpk('zpk',[1e3],[10],100)*myzpk('zpk',[1e3],[100],10);
Act_AOM = 10e6;
Act_AOM_X = Act_AOM*(1+asym/2);
Act_AOM_Y = Act_AOM*(1-asym/2);

% Low frequency
% G_GrM_servo = 2e+2*0;            % F_MASS servo: gain
% pGrM_servo_1 = 2*pi*   0;       % F_MASS servo: pole
% zGrM_servo_1 = 2*pi*  10;       % F_MASS servo: zero
% pGrM_servo_2 = 2*pi*   0;       % F_MASS servo: pole
% zGrM_servo_2 = 2*pi*  10;       % F_MASS servo: zero
% zGrM_servo_3 = 2*pi*  10;       % F_MASS servo: zero
% pGrM_servo_3 = 2*pi* 100;       % F_MASS servo: pole
% pGrM_servo_4 = 2*pi* 5e+2;      % F_MASS servo: pole
% pGrM_servo_5 = 2*pi* 5e+2;      % F_MASS servo: pole
% 
% Filt_mass = zpk([-zGrM_servo_1 -zGrM_servo_2 -zGrM_servo_3],[-pGrM_servo_1 -pGrM_servo_2 -pGrM_servo_3 -pGrM_servo_4 -pGrM_servo_5],G_GrM_servo*pGrM_servo_4*pGrM_servo_5);
% Filt_mass = zpk([-zGrM_servo_1 -zGrM_servo_2 -zGrM_servo_3],[-pGrM_servo_1 -pGrM_servo_2 -pGrM_servo_3 -pGrM_servo_4 -pGrM_servo_5],G_GrM_servo*pGrM_servo_4*pGrM_servo_5);
num = [(5.0e-6)*2*m2Hz*2*pi*2*pi];
den = [1 2*pi/10 4*pi*pi];
Act_mass = tf(num,den);


%Cavity
Changing_unit1 = c/L/532e-9;
num1 = [0.01*pi*pi];
den1 = [1 0.1*pi 0.01*pi*pi];

num2 = [4*pi*pi];
den2 = [1 2*pi/10 4*pi*pi];

inverted_pend = tf(num1,den1);
Pendulum =  tf(num2,den2);

dataH = load('./Noises/typeA20Kvibisoratio_with_IPdamp_L.dat'); 
dataV = load('./Noises/typeA20Kvibisoratio_V.dat'); 

ggH = interp1(dataH(:,1), dataH(:,2), freq, 'linear');
phH = interp1(dataH(:,1), dataH(:,3), freq, 'linear');
ggV = interp1(dataV(:,1), dataV(:,2), freq, 'linear');
phV = interp1(dataV(:,1), dataV(:,3), freq, 'linear');
for ii = 1:length(freq)
        if isnan(ggH(ii))
            if freq(ii) < 0.1
                ggH(ii) = 1;
            else
                ggH(ii) = 1e-36;
            end    
        end
        if isnan(phH(ii))
            if freq(ii) < 0.1
                phH(ii) = 0;
            else
                phH(ii) = 0;
            end    
        end       
        if isnan(ggV(ii))
            if freq(ii) < 0.1
                ggV(ii) = 1;
            else
                ggV(ii) = 1e-18./freq(ii).^9;
            end    
        end
        if isnan(phV(ii))
            if freq(ii) < 0.1
                phV(ii) = 0;
            else
                phV(ii) = -90;
            end    
        end
        
        %if freq(ii) < 0.1
        %    ggH(ii) = 1;
        %elseif freq(ii) < 0.4
        %    ggH(ii) = 0.1./freq(ii);
        %end    
            
end


for mir = {'ETMX','ETMY'}
    mir = char(mir);
    Susp([mir,'_Seism_TM']) = frd(ggH.*exp(i*phH/180*pi),freq,'FrequencyUnit','Hz');  % Seismic noise to TM [m/m]
    Susp([mir,'_Seism_Vert']) = frd(ggV.*exp(i*phV/180*pi),freq,'FrequencyUnit','Hz');  % Seismic noise to TM from vertical coupling [m/m]
end
VertCoup = 0.01;    % vertical coupling
CMRR_arm = 1;




SW(1) = 1; 
SW(2) = 1;
SW(3) = 1;
SW(4) = 1;
SW(5) = 1;
SW(6) = 1;
SW(7) = 1;

%% Plot expected TFs

%if plot_TFs

%%%% to create a bode plot with the freqeuncy axis in Hz %%%%
set(cstprefs.tbxprefs,'FrequencyUnits','Hz')

figure(99)
[A,B,C,D] = linmod('GREEN_CARM_DARM');
tfs = ss(A,B,C,D);
TF_Arm=tfs(1,17);
plotbode(freq,TF_Arm/m2Hz);
subplot(2,1,1)
[Due_to_IMC,Due_to_IMCp] = mybode(CARM_Cavity_Pole*(1-myzpk('zpk',[],[Cav('Cpole_IMC')],1)),freq);
loglog(freq,Due_to_IMC/2);
ylim([1e-6,1e-2]);
xlim([1e-3,1e2]);
set(gca,'YTick',logspace(-6,-2,5));
set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
subplot(2,1,2)
semilogx(freq,Due_to_IMCp);
xlim([1e-3,1e2]);
set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
legend('Contribution from Arm Length','Due to IMC Cavity Pole Effect')
saveas(gcf,'./results/Contribution_from_Arm_Length_Fluctuation.png')
[mag, phs] = mybode(TF_Arm/m2Hz, freq);
data(:,1) = freq;
data(:,2) = mag;
data(:,3) = phs;
filename = 'results/Contribution_from_Arm_Length_Fluctuation.dat';
fileID = fopen(filename,'w');
fprintf(fileID,'%6.10f %.16e %12.30f \r\n',data');
fclose(fileID);
clear data

% figure(100)
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% aaaa=tfs(1,2);
% bode(aaaa)
% grid on
% legend('TM disp. contribution')
% 
% SW(1) = 0; 
% SW(7) = 0;
% 
% figure(101)
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% aaaa=tfs(2,3);
% bode((1/aaaa)-1)
% grid on
% legend('PLL gain')
% 
% figure(102)
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% aaaa=tfs(3,4);
% bode(aaaa)
% grid on
% legend('PLL follow')
% 
% SW(1) = 1; 
% SW(7) = 1;
% 
% figure(103)
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% aaaa=tfs(1,4);
% bode(aaaa)
% grid on
% legend('contribution from PSL')
% 
% %figure(104)
% 
% 
% %figure(105)
% 
% 
% % DOF Switches
% loopNames = {'total','SUSP','AOM','IR total','Add','MCL','IMC_AOM'};
% SW = ones(1,length(loopNames));    % turn on the loops
% swtot = 1;  % switches for the total loop
% swact = 3:4;  % switches for each actuator loop
% 
% OLTF=[];
% % OLTF for total loop
% SW(swtot) = zeros(1,length(swtot));
% SW(swact) = ones(1,length(swact));
% [A,B,C,D]=linmod('GREEN_CARM_DARM');
% systm=ss(A,B,C,D);
% OLTF=[OLTF,-1*systm(swtot+4,swtot+4,:)];
% % OLTF for each actuator loop
% 
% %SW = zeros(1,length(loopNames));
% SW(swtot) = ones(1,length(swtot));
% SW(swact) = zeros(1,length(swact));
% [A,B,C,D]=linmod('GREEN_CARM_DARM');
% for kk=swact
% systm=ss(A,B,C,D);
%     OLTF=[OLTF,-1*systm(kk+4,kk+4,:)];
% end
% 
% % Common green lock loop
% 
% set(0, 'DefaultAxesFontSize',10);
% figure(110)
% plotbode(freq,OLTF);
% subplot(2,1,1)
% ylim([1e-1,1e5]);
% %xlim([freq(1),freq(end)]);
% xlim([0.1,1e6]);
% legend(loopNames{swtot},loopNames{swact});
% set(gca,'YTick',logspace(-1,5,7));
% set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
% subplot(2,1,2)
% %xlim([freq(1),freq(end)]);
% xlim([0.1,1e6]);
% set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
% legend(loopNames{swtot},loopNames{swact});
% saveas(gcf,'./results/green_OLTF.png')
% 
% SW = ones(1,length(loopNames));
% SW(swact) = ones(1,length(swact));
% 
% 
% %%%%% IR path, additive offset and MCL path
% swtot = 4;  
% swact = 5:6; 
% %Filt_GR1 = myzpk('zpk',[],[4;100e3],1e-6);
% 
% OLTF=[];
% % OLTF for total loop
% SW(swtot) = zeros(1,length(swtot));
% SW(swact) = ones(1,length(swact));
% [A,B,C,D]=linmod('GREEN_CARM_DARM');
% systm=ss(A,B,C,D);
% OLTF=[OLTF,-1*systm(swtot+4,swtot+4,:)];
% % OLTF for each actuator loop
% 
% %SW = zeros(1,length(loopNames));
% SW(swtot) = ones(1,length(swtot));
% SW(swact) = zeros(1,length(swact));
% [A,B,C,D]=linmod('GREEN_CARM_DARM');
% for kk=swact
% systm=ss(A,B,C,D);
%     OLTF=[OLTF,-1*systm(kk+4,kk+4,:)];
% end
% 
% set(0, 'DefaultAxesFontSize',10);
% figure(111)
% plotbode(freq,OLTF);
% subplot(2,1,1)
% ylim([1e-1,1e9]);
% %xlim([freq(1),freq(end)]);
% xlim([0.1,1e5]);
% legend(loopNames{swtot},loopNames{swact});
% set(gca,'YTick',logspace(-1,11,13));
% set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
% subplot(2,1,2)
% %xlim([freq(1),freq(end)]);
% xlim([0.1,1e5]);
% set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
% legend(loopNames{swtot},loopNames{swact});
% saveas(gcf,'./results/ALS_CARM_TF.png')
% 
% SW = ones(1,length(loopNames));
% SW(swact) = ones(1,length(swact));
% 
% 
% % Differential green lock loop
% figure(113)
% SW(1) = 0;
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% D_green_tot = tfs(14,15);
% SW(1) = 1;
% 
% SW(2) = 0;
% SW(3) = 0;
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% D_green_AOM = tfs(15,16);
% D_green_susp = tfs(6,6);
% SW(2) = 1;
% SW(3) = 1;
% opts = bodeoptions('cstprefs');
% opts.YLimMode = 'Manual';
% ylims{1} = [-20 60];
% ylims{2} = [-180 180];
% opts.YLim = ylims;
% hold on
% bodeplot(-1*D_green_tot,opts)
% bodeplot(-1*D_green_AOM,opts)
% bodeplot(-1*D_green_susp,opts)
% grid on
% legend('DARM_total','AOM','susp')
% xlim([0.1 1e6]);
% 
% % DARM loop TFs
% figure(114)
% %Filt_darm = myzpk('zpk',[10],[100],1)*myzpk('zpk',[.3],[3],.10);
% %Filt_GR1 = myzpk('zpk',[],[4;100e3],.1);
% SW(2) = 0;
% %SW(3) = 0;
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% %D_AOM=tfs(15,16);
% D_susp=tfs(6,6);
% opts = bodeoptions('cstprefs');
% %ylims = getoptions(bodeplot(-1*D_AOM),'YLim');
% opts.YLimMode = 'Manual';
% ylims{1} = [-20 100];
% ylims{2} = [-180 180];
% opts.YLim = ylims;
% hold on
% %bodeplot(-1*D_AOM,opts)
% bodeplot(-1*D_susp,opts)
% %bodeplot(1/(1-1*D_susp),opts)
% %bodeplot(-1*(D_AOM+D_susp),opts)
% grid on
% legend('DARM')
% xlim([0.1 1e5]);
% saveas(gcf,'./results/ALS_DARM_TF.png')
% %Filt_darm = myzpk('zpk',[10],[100],1);
% %Filt_GR1 = myzpk('zpk',[],[4;100e3],0);
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% D_susp_boost=tfs(6,6);
% SW(2) = 1;
% %SW(3) = 1;
% 
% % % Hand-over from AOM to DARM
% % figure(115)
% % opts = bodeoptions('cstprefs');
% % %ylims = getoptions(bodeplot(-1*D_AOM),'YLim');
% % opts.YLimMode = 'Manual';
% % ylims{1} = [-20 60];
% % ylims{2} = [-180 180];
% % opts.YLim = ylims;
% % hold on
% % for ii = [-3:1:0]
% %     bodeplot(-1*(D_AOM + D_susp*10^ii),opts)
% % end
% % for ii = -1*[0.5:0.5:1.5]
% %     bodeplot(-1*(D_AOM*10^ii + D_susp),opts)
% % end
% % bodeplot(-1*D_susp_boost,opts)
% % legend('1','2','3','4','5','6','7','8')
% % grid on
% % xlim([0.1 1e4]);
% % saveas(gcf,'./results/DARM_AOM2Susp_handover.png')
% 
% 
% % SW(1) = 0; 
% % figure(106)
% % [A,B,C,D] = linmod('GREEN_CARM_DARM');
% % tfs = ss(A,B,C,D);
% % aaaa=tfs(5,5);
% % bode(aaaa)
% % grid on
% % legend('Green OLG')
% % SW(1) = 1; 
% 
% SW(4) = 0; 
% SW(7) = 0; 
% figure(107)
% [A,B,C,D] = linmod('GREEN_CARM_DARM');
% tfs = ss(A,B,C,D);
% aaaa=tfs(7,4);
% bode(aaaa*Act_AOM/2)
% grid on
% legend('Green as a IR freq sensor')
% SW(4) = 1; 
% SW(7) = 1;
% 
% %figure(108)
% %[A,B,C,D] = linmod('GREEN_CARM_DARM');
% %tfs = ss(A,B,C,D);
% %aaaa=tfs(8,4);
% %bode(Filt_GR*Filt_IMC*Filt_MCL*Act('MCEsus')*Filt_GR)
% %grid on
% %legend('MCL path')
% 
% % SW(5) = 0; 
% % SW(6) = 0;
% % %CMS_SW_IMC('IN2EN') = 1;
% % figure(108)
% % [A,B,C,D] = linmod('GREEN_CARM_DARM');
% % tfs = ss(A,B,C,D);
% % aaaa=tfs(3,9);
% % bode(aaaa)
% % hold on
% % [A,B,C,D] = linmod('GREEN_CARM_DARM');
% % tfs = ss(A,B,C,D);
% % aaaa1=tfs(3,10);
% % bode(aaaa1)
% % hold on
% % bode(aaaa+aaaa1)
% % grid on
% % legend('Additive offset','MCL path','sum')
% % SW(5) = 1; 
% % SW(6) = 1; 
% %CMS_SW_IMC('IN2EN') = 0;
% 
% % SW(5) = 0;
% % SW(6) = 0; 
% % SW(7) = 0;
% % figure(99)
% % [A,B,C,D] = linmod('GREEN_CARM_DARM');
% % tfs = ss(A,B,C,D);
% % aaaa=tfs(11,11);
% % bode(aaaa)
% % grid on
% % legend('IMC AOM path')
% % SW(5) = 1;
% % SW(6) = 1; 
% % SW(7) = 1;
% end
% SW = ones(1,length(loopNames));
% 
% 
% %% Define some parameters and get live parts parameters
% %freq = logspace(-3,6,100000);
% liveModel = 'GREEN_CARM_DARM';
% dof = 'CARM';    % name of DOF to plot NB
%  startTime = 1078250000;   % start GPS time
%  durationTime = 512;
%  IFO = 'K1';
%  site = 'kamioka';
% 
% %duration = 64;  % data get time duration
% freqsamp = 16384;   % sampling frequency
% freqmin = 0.1;  % minimum frequency (= frequency reslution)
% Ndata = ceil(freqsamp/freqmin);
% ndata = 2^nextpow2(Ndata);
% duration2 = 64;  % data get time duration
% freqsamp2 = 2048;   % sampling frequency
% freqmin2 = 0.1;  % minimum frequency (= frequency reslution)
% Ndata2 = ceil(freqsamp2/freqmin2);
% ndata2 = 2^nextpow2(Ndata2);
%  
% % Try setting different NDS server if you couldn't get data
% % setenv('LIGONDSIP','h1nds1:8088');
% % mdv_config;
% 
% % load cached outputs
% loadFunctionCache()
% 
% % get live parts parameters
% %liveParts(liveModel, startTime, durationTime, freq)
% 
% 
% Noise('SHG') = 1e-5.*freq;  % SHG frequency noise in [Hz/rtHz]
% %Noise('Fiber') = 1.;  % Green fiber frequency noise in [Hz/rtHz]
% Noise('Fiber') = sqrt((2e-3)^2 + (3e-2./freq.^2).^2) * sqrt(50/5);  % Green fiber frequency noise in [Hz/rtHz] klog 5417
% Noise('Shot noise green') = 8e-6; % Shot noise in [Hz/rtHz]
% 
% noise = load('./Noises/KamiokaSeismicHighNoise.txt'); % file from Suspension modeling svn
% temp_noise = interp1(noise(:,1), noise(:,2), freq, 'linear');
%     for ii = 1:length(freq)
%         if isnan(temp_noise(ii))
%             temp_noise(ii) = 1.5e-9.*freq(ii).^-2;
%         end
%     end
% Noise('Seismic test mass') = temp_noise;% Seismic noise of test masses in [m/rtHz]
% 
% noise = load('./Noises/KamiokaSeismicNoise_ArmLength.txt'); % Arm length displacement data given by Miyo-kun
% temp_noise = interp1(noise(:,1), noise(:,2), freq, 'linear');
%     for ii = 1:length(freq)
%         if isnan(temp_noise(ii))
%             temp_noise(ii) = 1.5e-9.*freq(ii).^-2*sqrt(2);
%         end
%     end
% Noise('Seismic arm length') = temp_noise; % Arm length displacement of test masses in [m/rtHz]
% 
% 
% 
% %Noise('VCO noise') = 0.00005./freq; % VCO noise of AOM path of green lock in [Hz/rtHz]  ????????
% %Noise('VCO noise') = 0.3; % VCO noise of AOM path of green lock in [Hz/rtHz]  ????????
% noise = load('./Noises/VCO_frequencynoise.txt'); % file from Suspension modeling svn
% temp_noise = interp1(noise(:,1), noise(:,2), freq, 'linear');
%     for ii = 1:length(freq)
%         if isnan(temp_noise(ii))
%             temp_noise(ii) = 0.06;
%         end
%     end
% Noise('VCO noise') = temp_noise; % klog 6552
% Noise('Shot noise IR') = 8e-7; % Shot noise in [Hz/rtHz]
% 
% Noise('PSL freq noise') = 0*freq./freq/10+8e-9*freq.^-2./(1+(2./freq).^-8)/26.65*299792458./1064e-9; % PSL freq noise in [Hz/rtHz]
% Noise('Prometheus freq noise') = 10000./freq; % PROMETHEUS freq noise in [Hz/rtHz]
% 
% Noise('LO noise') = 0.00005./freq; % LO noise of PLL loop in [Hz/rtHz]  ????????
% Noise('Shot noise PLL') = 2.5e-8; % Shot noise in [rad/rtHz]
% Noise('Electronic noise PLL') = 100e-9; % Electronic noise of PLL loop in [V/rtHz]
% Noise('Electronic noise PDH') = 100e-9; % Electronic noise of PDH loop in [V/rtHz]
% Noise('PD noise PDH') = 2.92e-11; % Dark noise of green RF PD in [W/rtHz] For example, Thorlabs PDA10A2 ???
% 
% 
% noise = load('./Noises/KamiokaSeismicHighNoise.txt'); % file from Suspension modeling svn
% temp_noise = interp1(noise(:,1), noise(:,2), freq, 'linear');
%     for ii = 1:length(freq)
%         if isnan(temp_noise(ii))
%             temp_noise(ii) = 1.5e-9.*freq(ii).^-2;
%         end
%     end
% Noise('seismic_IMC') = temp_noise;
% 
% Noise('act_AOM') = 3e-8; % VCO  noise of FSS loop in [V/rtHz]
% 
% load('Sensor_Noise_RefCav.mat')
%     temp_noise =...
%         interp1(Sensor_Noise_RefCav('ff_KOACH_off'),Sensor_Noise_RefCav('KOACH_off'),freq);
%     for ii = 1:length(freq)
%         if isnan(temp_noise(ii))
%             temp_noise(ii) = 8.071e-5*(15./(freq(ii)/0.1+1).^0.6./(freq(ii)/2000+1)./(freq(ii)/3000+1).*(freq(ii)/700+1));
%         end
%     end
% Noise('sensor_RefCav') = temp_noise; % RefCav unknown sensing noise in [V/rtHz]
% 
% SW(1) = 1; 
% 
% %% Compute noises and save cache
% % Compute noises
% [noises, sys] = nbFromSimulink(liveModel, freq, 'dof', dof);
% 
% % save cached outputs
% saveFunctionCache();
% 
% % ----------- comment out because of error from plotcumulativeRMS2---------
% 
% % %% Make a quick NB plot
% % if plot_NBs
% % disp('Plotting noises')
% % nb = nbGroupNoises(liveModel, noises, sys);
% % 
% % % Get noise data from DAQ. Put NdNoiseSource block with DAQ channel
% % % specified. Put something (e.g. 1) in ASD parameter of that block.
% % %nb = nbAcquireData(liveModel, sys, nb, startTime, durationTime);
% % 
% % %nb.sortModel();
% % %matlabNoisePlot(nb);
% % %figure(1)
% % %grid on;
% % %axis tight;
% % %ylabel('Mag (m/sqrt(Hz))');
% % %xlabel('Frequency (Hz)');
% % %ylim([1e-22,1e-10]);
% % %xlim([1,1e4]);
% % 
% % %%figure(2);
% % %matlabNoisePlot(nb);
% % %%legend('Location','southwest')
% % %%hold on
% % %plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1]);
% % %grid on;
% % %axis tight;
% % %ylabel('Mag (Hz/sqrt(Hz))','FontSize',20);
% % %xlabel('Frequency (Hz)','FontSize',20);
% % %title('Frequency noises');
% % %xlim([1e-3,1e6]);
% % %%ylim([1e-22,1e-10]);
% % %ylim([1e-10,1e2]);
% % %leg = legend(gca);
% % %legend({leg.String{:},'RMS'},'Interpreter','None','Location','southwest');
% % %saveas(gcf,'./results/nb.fig')
% % 
% % nb.sortModel();
% % matlabNoisePlot(nb);
% % 
% % figure(2)
% % xlim([1e-3,1e6]);
% % ylim([1e-10,1e2]);
% % %plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1]);
% % leg = legend(gca);
% % %legend({leg.String{:},'RMS'},'Interpreter','None','Location','southwest');
% % saveas(gcf,'./results/Green_noiseNB.fig')
% % clear leg
% % 
% % figure(3)
% % xlim([1e-3,1e6]);
% % ylim([1e-10,1e2]);
% % %plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1]);
% % leg = legend(gca);
% % %legend({leg.String{:},'RMS'},'Interpreter','None','Location','southwest');
% % saveas(gcf,'./results/IR_noiseNB.fig')
% % clear leg
% % 
% % figure(4)
% % xlim([1e-3,1e6]);
% % ylim([1e-10,1e2]);
% % %plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1]);
% % leg = legend(gca);
% % %legend({leg.String{:},'RMS'},'Interpreter','None','Location','southwest');
% % saveas(gcf,'./results/Seismic_noiseNB.fig')
% % 
% % figure(5)
% % xlim([1e-3,1e6]);
% % ylim([1e-10,1e2]);
% % %plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1]);
% % leg = legend(gca);
% % %legend({leg.String{:},'RMS'},'Interpreter','None','Location','southwest');
% % saveas(gcf,'./results/PLL_noiseNB.fig')
% % 
% % figure(1)
% % xlim([1e-3,1e6]);
% % ylim([1e-10,1e2]);
% % plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1],0.1);
% % leg = legend(gca);
% % legend({leg.String{:},'RMS'},'Interpreter','None','Location','southwest');
% % set(gca,'YTick',logspace(-10,2,13));
% % set(gca,'XTick',logspace(log10(freq(1)),log10(freq(end)),log10(freq(end))-log10(freq(1))+1));
% % saveas(gcf,'./results/ALS_NB.fig')
% % saveas(gcf,'./results/ALS_NB.png')
% % 
% % end
% % 
% % %% Actuators saturation check
% % act = 'FSS_AOM'; 
% % if plot_Saturations
% % disp('Checking saturation')
% % % Compute noises
% % [noises_AOM, sys_AOM] = nbFromSimulink(liveModel, freq, 'dof', act);
% % 
% % % save cached outputs
% % saveFunctionCache();
% % 
% % % plot
% % nb = nbGroupNoises(liveModel, noises_AOM, sys_AOM);
% % nb.sortModel();
% % matlabNoisePlot(nb);
% % 
% % figure(6)
% % xlim([1e-3,1e6]);
% % ylim([1e-10,1e-1]);
% % plotcumulativeRMS2(nb.sumNoise.f,nb.sumNoise.asd,[1,0,1]);
% % 
% % end
% % 
% % %% plot expected curve from calculation
% % 
% % %[mag,ph]=bode((Gol)/(1+Gol),2*pi*freq);
% % %loglog(freq,squeeze(mag),'b.')
% % %hold on
% % 
% % %[mag,ph]=bode(1/Sen,2*pi*freq);
% % %loglog(freq,freq./freq/Sen,'r.')
% % ---------------------------------------
