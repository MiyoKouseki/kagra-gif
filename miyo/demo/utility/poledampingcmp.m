function poledampingcmp(sys,sys2)

%% Information
% SAS Model: Type-A Adv. Virgo-like structure
% Plots    : Pole-Zero Plot


%% Pole-Zero List Feedback

vecpole=pole(sys);
vecpole=vecpole(real(vecpole)<0);
vecpole=vecpole(imag(vecpole)>1e-6);
vecpolei=imag(vecpole)/2/pi;
vecpoler=-1./real(vecpole);
[vecpolei,numpolei]=sort(vecpolei);
vecpoler=vecpoler(numpolei);
% vecpolec=[vecpolei,vecpoler]

vecpole2=pole(sys2);
vecpole2=vecpole2(real(vecpole2)<0);
vecpole2=vecpole2(imag(vecpole2)>1e-6);
vecpolei2=imag(vecpole2)/2/pi;
vecpoler2=-1./real(vecpole2);
[vecpolei2,numpolei2]=sort(vecpolei2);
vecpoler2=vecpoler2(numpolei2);
% vecpolec=[vecpolei,vecpoler]


%% Q Value
freqvecpole=logspace(-2,2.5,10);
% yvecQ1=1/pi./freqvecpole;
yvecQ10=10/pi./freqvecpole;
% yvecQ100=100/pi./freqvecpole;
yvecQ1000=1000/pi./freqvecpole;
yvecT60=60*freqvecpole./freqvecpole;



%% Freq-Damping LogLog
fig=figure;
  loglog(vecpolei,vecpoler,'ko',...
       vecpolei2,vecpoler2,'m*',...
       freqvecpole,yvecQ10,'--g',...
       freqvecpole,yvecQ1000,'--y',...
       freqvecpole,yvecT60,'--r',...
       'MarkerFaceColor','k','LineWidth',2);
  grid on;
  legend('CONTROL OFF','CONTROL ON','Q=10','Q=1000','1 min.')
  title('Frequency vs Damping Time','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
  ylabel('Damping Time [sec]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
  xlabel('Frequency [Hz]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
  set(gca,'FontSize',12,'FontName','Times New Roman')
  set(fig,'Position', [0 50 800 650])
  set(fig,'Color','white')
  xlim([1e-2,3e2])


end