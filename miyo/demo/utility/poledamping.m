function poledamping(sys)

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

% vecpole=pole(sys);
% vecpole=vecpole(real(vecpole)<0);
% vecpoleX=vecpole(imag(vecpole)>1e-6);
% vecpoleX=vecpole(real(vecpoleX)<0);
% vecpoleiX=imag(vecpoleX)/2/pi;
% vecpolerX=+1./real(vecpoleX);
% [vecpoleiX,numpoleiX]=sort(vecpoleiX);
% vecpolerX=vecpoler(numpoleiX);


%% Q Value
freqvecpole=logspace(-2,2.5,10);
% yvecQ1=1/pi./freqvecpole;
yvecQ10=10/pi./freqvecpole;
% yvecQ100=100/pi./freqvecpole;
yvecQ1000=1000/pi./freqvecpole;
yvecT60=60*freqvecpole./freqvecpole;



%% Freq-Damping LogLog
figure
  loglog(vecpolei,vecpoler,'ko',...
      ...vecpoleiX,vecpolerX,'ro',...
       freqvecpole,yvecQ10,'--g',...
       freqvecpole,yvecQ1000,'--y',...
       freqvecpole,yvecT60,'--r',...
       'MarkerFaceColor','k','LineWidth',2);
  grid on;
  legend('System Resonace','Q=10','Q=1000','1 min.')
  title('Frequency vs Damping Time','FontSize',12,'FontWeight','bold','FontName','Cambria')
  ylabel('Damping Time [sec]','FontSize',12,'FontWeight','bold','FontName','Cambria')
  xlabel('Frequency [Hz]','FontSize',12,'FontWeight','bold','FontName','Cambria')
  set(gca,'FontSize',12,'FontName','Cambria')
  xlim([1e-2,3e2])


end