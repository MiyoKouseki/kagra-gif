%%main
function getqt160115(sysc0,sysc)

vecpole0=pole(sysc0);
vecpole0=vecpole0(real(vecpole0)<0);
vecpole0=vecpole0(imag(vecpole0)>1e-6);
vecpole0i=imag(vecpole0);
vecpole0r=real(vecpole0);
[vecpole0i,numpole0i]=sort(vecpole0i);
vecpole0r=vecpole0r(numpole0i);
vecpole0=[vecpole0i,-vecpole0r];

vecpolec=pole(sysc);
vecpolec=vecpolec(real(vecpolec)<0);
vecpolec=vecpolec(imag(vecpolec)>1e-6);
vecpoleci=imag(vecpolec);
vecpolecr=real(vecpolec);
[vecpoleci,numpoleci]=sort(vecpoleci);
vecpolecr=vecpolecr(numpoleci);
vecpolec=[vecpoleci,-vecpolecr];

%% FREQUENCY
freq =logspace(-2,3,1001);

fig=figure;
grid on
%loglog(vecpole0(:,1)/2./pi,1./vecpole0(:,2),'bo',...
%	   vecpolec(:,1)/2./pi,1./vecpolec(:,2),'ro','MarkerSize',2,'MarkerFaceColor','r')
loglog(vecpole0(:,1)/2./pi,1./vecpole0(:,2),'b.',...
	   vecpolec(:,1)/2./pi,1./vecpolec(:,2),'r.',...
	   freq,1000/pi./freq,'--y',...
       freq,10/pi./freq,'--g',...
       freq,60,'--m',...
	   'MarkerSize',10)

grid on
title('Quality factor with controls ON and OFF','FontSize',12,'FontWeight','bold','FontName','Times New Roman',...
    'interpreter','none')
ylabel('1/e damping time [sec]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
xlabel('Frequency [Hz]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
set(gca,'FontSize',12,'FontName','Times New Roman')
legend('Control OFF','Control ON','Q = 1000','Q = 10','1 min.')
ylim([1e-1 1e5])
xlim([0.01,1000])
set(fig,'Color','white')