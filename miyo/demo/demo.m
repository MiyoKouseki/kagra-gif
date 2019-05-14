%% preliminary
clear all
close all
addpath('utility')

%% state-space
% -------------------- make state-space model ---------------------
k=100;
m=1;

mat1=[0,-k/m;1,0];
mat2=[k/m,1;0,0];
mat3=[0,1];
mat4=[0,0];

%% system (no control)
% ------------------  make non-controlled system ------------------ 
servo=0;
gain_act=1e+2;

st=linmod('testmdl');
sysc0 = ss(st.a,st.b,st.c,st.d,'inputname',{'GND','F','NOISE'},'outputname',{'OUTPUT'});

% ------ plot transfer functions of non-controlled system ---------
freq=logspace(-2,2,1001);
bodesusplot(sysc0,'GND','OUTPUT',freq) % plot displacement-TF 
%export_fig('figures/disp_TF_woctrl.pdf')
bodesusplot(sysc0,'F','OUTPUT',freq) % plot forced-TF
%export_fig('figures/forced_TF_woctrl.pdf')

%% system (controlled)
% -------------------- set servo filter ---------------------------
num=[10,0];
den=[0.001,1];
%servo = tf(num,den);
tf1=zpk(0,-100,1.5);
tf2=zpk(0,[-100,-100],7.5e1);
tf3=zpk([],-0.3,1);
% --------- high-pass filter -------------------------------------
servo=tf1;
% --------- low-pass filter --------------------------------------
%servo=tf3;


% --------------- plot bode plot of servo filters ----------------
mybodeplot({tf1,tf2,tf3,servo},freq,...
	       {'tf1','tf2','tf3','servo'},'servo filter')
%export_fig('figures/servo_filters.pdf')

% -------------------- plot bode plot of OLTF --------------------
bodesusplotcmpoptOLTF(sysc0,...
     {'F','OUTPUT'},freq,'ylim',[1e-5,1e4],...
     'calibration',{gain_act*servo},...
     'unit1','1','title','Open Loop Gain',...
     'legend',{'OLTF'});
%export_fig('figures/OLTF.pdf')


% ------------------- load noise data ----------------------------
nosem=importdata('noise/OSEMnoiseworstproto_disp.dat'); % um/rtHz
nosem1=interp1(nosem(:,1),nosem(:,2)*1e-6,freq); % m/rtHz

data_seism = importdata('noise/KamiokaSeismicHighNoise.dat'); % m/rtHz
noise_seism = interp1(data_seism(:,1),data_seism(:,2),freq')'; % m/rtHz


% -----------------  make controlled system ----------------------
st=linmod('testmdl');
sysc= ss(st.a,st.b,st.c,st.d,'inputname',{'GND','F','NOISE'},'outputname',{'OUTPUT'});


% ------- plot displacement/forced TF with/without control -------
%bodesusplotcmp(sysc0,sysc,'GND','OUTPUT',freq)
%export_fig('figures/disp_TF_ctrlcomp.pdf')
bodesusplotcmp(sysc0,sysc,'F','OUTPUT',freq)
%export_fig('figures/forced_TF_ctrlcomp.pdf')

% ---- calculate seismic noise contribution into disp. wo ctrl ----
[mag0seis,~]=bodesus(sysc0,'GND','OUTPUT',freq);
output_seis_noise_noctrl=mag0seis.*noise_seism;

rms_seis =makerms(freq, output_seis_noise_noctrl);


% --- calculate sensor noise contribution into disp. with control ---
[magosem,~]=bodesus(sysc,'NOISE','OUTPUT',freq);
%bodesusplot(sysc,'NOISE','OUTPUT',freq)
output_osem_noise=magosem.*nosem1;

rms_output_osem =makerms(freq, output_osem_noise);


% ---- calculate seismic noise contribution into disp. with ctrl ----
[magseis,~]=bodesus(sysc,'GND','OUTPUT',freq);
%bodesusplot(sysc,'NOISE','OUTPUT',freq)
output_seis_noise=magseis.*noise_seism;
magnTot=sumpsd({output_osem_noise, output_seis_noise}); %ALL Noise

rms_output_seis =makerms(freq, magnTot);


% ------ plot control noise contribution into TM displacement --------
mypsdplotopt({noise_seism,output_seis_noise_noctrl,magnTot,rms_seis,rms_output_seis},freq,...
    'title','control noise to TM',...
    'legend',{'GND','non-controlled output','controlled output','seismic noise (RMS)','controlled output (RMS)'},...
    'color',{'k-','b-','r-','c--','m--'},...
    'ylim',[1e-15,1e-4],'ylabel','Magnitude [m/rtHz] or [m]')
%export_fig('figures/control_noise.pdf')


% ---- plot control noise contribution into TM displacement (2) ------
mypsdplotopt({noise_seism, output_seis_noise_noctrl, output_osem_noise, magnTot},freq,...
    'title','control noise to TM (seonsor noise)',...
    'legend',{'GND','non-controlled output','OSEM noise','controlled output'},...
    'color',{'k-','b-','g-','r-'},...
    'ylim',[1e-15,1e-4],'ylabel','Magnitude [m/rtHz]');
%export_fig('figures/control_noise_sensnoise-contribution.pdf')


% % ------ plot decay-time constant for each resonant frequency --------
% getqt_damp(sysc0,sysc);
% %export_fig('figures/qfactors.pdf');
% 
% 
% % ------------------ calculate impulse response ----------------------
% [yc0,t] = impulse(sysc0,0:5e-3:15);
% [yc,t] = impulse(sysc,0:5e-3:15);

% --------------------- plot impulse response ------------------------
% fig=figure;
% plot(t,yc0(:,1,2),'b-','LineWidth',1.5);
% hold on
% plot(t,yc(:,1,2),'r-','LineWidth',1.5);
% hold off
% grid on
% ylim([-15 15])
% title('Impulse resopnse','FontSize',12,'FontWeight','bold','FontName','Times New Roman',...
%     'interpreter','none')
% xlabel('Time [sec]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
% ylabel('Amplitude [a.u.]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
% legend({'no control','with control'},'FontSize',12,'FontName','Times New Roman',...
%     'interpreter','none')
% set(gca,'FontSize',12,'FontName','Times New Roman')
% set(fig,'Color','white')
% %export_fig('figures/impulse_response.pdf');
% 
% % ----------- other tips: build nyquist/pole-zero plots ------------
% fig=figure;
% nyquist(sysc)
% fig=figure;
% pzplot(sysc0)
% fig=figure;
% grid on
% pzplot(sysc)
% grid on
