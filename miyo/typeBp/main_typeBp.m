%% 
clear all;                     % Clear workspace
close all;                     % Close plot windows

%% MODEL IMPORT
load('typeBp_ss.mat');  % Import state space model in current work space.
param_PR3_noctr;        % Import parameter from '.m' file 


%%
slx_fname = 'TypeBp';   
st      = linmod(slx_fname); 
save('linmod.mat','st')
invl    = strrep(st.InputName, [slx_fname,'/'],'');
outvl   = strrep(st.OutputName,[slx_fname,'/'],'');
sysc0   = ss(st.a,st.b,st.c,st.d,'inputname',invl,'outputname',outvl);

disp(invl)

%% FREQUENCY SET
freq=logspace(-2,2.5,1001);
colorarg={'-r','-b','bo'}
data=importdata('measurement/TF_TML.txt');


%%
inv='actLTM'
outv='OpLev_LTM'
titlearg=['Transfer Function Bode Plot',' from ',inv,' to ',outv]
unit='m'
ylabelarg=['Magnitude ',unit]
nin=strcmp(sysc0.InputName,inv);
nout=strcmp(sysc0.OutputName,outv);
% TRANSFER FUNCTION
calib=1
[mag,phs] = mybode(sysc0(nout,nin)*calib,freq);

fig=figure;
subplot(5,1,[1 2 3])
loglog(freq,mag,colorarg{1},data(:,1),data(:,2),colorarg{2},'LineWidth',2)
grid on
title(titlearg,'FontSize',12,'FontWeight','bold','FontName','Times New Roman',...
    'interpreter','none')
ylabel(ylabelarg,'FontSize',12,'FontWeight','bold','FontName','Times New Roman')
set(gca,'FontSize',12,'FontName','Times New Roman')
fg_y=0;
if fg_y; ylim(ylimarg); end;
xlim([freq(1),freq(end)])
legendarg={'model','measurement'}
legend(legendarg)
  
subplot(5,1,[4 5])
semilogx(freq,phs,colorarg{1},data(:,1),data(:,3),colorarg{3},...
    'LineWidth',2,'MarkerSize',2)
grid on
ylim([-180 180])
xlim([freq(1),freq(end)])
ylabel('Phase [deg]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
xlabel('Frequency [Hz]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
set(gca,'FontSize',12,'FontName','Times New Roman')
set(gca,'YTick',-180:90:180)
positionarg=[50, 50, 850, 650]
set(fig,'Position', positionarg)
set(fig,'Color','white')
  
%%

% 
% 
% %% TRANSFER FUNCTION TM
% data_LTM=importdata('measurement/TF_TML.txt');
% 
% 
% 
% 
% bodesusplotmeascmp(sysc0,'actLTM','OpLev_LTM',freq1,data_LTM,...
%                    'ylim',[1e-5,1e3],'unit1','1','color',{'-r','-b','-b'},...
%                    'title','Transfer function from LTM actuator to LTM sensor');
%   
%               
% %%               
% saveas(gcf, 'TFcmp_LTM_170531', 'pdf')
% 
