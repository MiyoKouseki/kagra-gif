function bodesusplotacc(sys,invl,outvl,freq)

nin=strcmp(sys.InputName,invl);
nout=strcmp(sys.OutputName,outvl);
[mag,phs] = mybode(-1*sys(nout,nin),freq);
mag=mag*2*pi.*freq*2*pi.*freq;

if strncmp(invl,'accL',1)||strncmp(invl,'accT',1)||strncmp(invl,'accV',1)
    unit1='m';
elseif strncmp(invl,'accR',1)||strncmp(invl,'accP',1)||strncmp(invl,'accY',1)
    unit1='rad';
else
    error('bodesusplotacc:InputError','Wrong input variables.')
end

invl2=invl(4:length(invl));

if strncmp(outvl,'L',1)||strncmp(outvl,'T',1)||strncmp(outvl,'V',1)
    unit2='m';
elseif strncmp(outvl,'R',1)||strncmp(outvl,'P',1)||strncmp(outvl,'Y',1)
    unit2='rad';
elseif strncmp(outvl,'senL',1)||strncmp(outvl,'senT',1)||strncmp(outvl,'senV',1)
    unit2='m';
elseif strncmp(outvl,'senR',1)||strncmp(outvl,'senP',1)||strncmp(outvl,'senY',1)
    unit2='rad';
elseif strncmp(outvl,'velL',1)||strncmp(outvl,'velT',1)||strncmp(outvl,'velV',1)
    unit2='(m/s)';
elseif strncmp(outvl,'velR',1)||strncmp(outvl,'velP',1)||strncmp(outvl,'velY',1)
    unit2='(rad/s)';
else
    unit2='1';
end

if  strcmp(unit1,'1')||strcmp(unit2,'1')
    unit='';
else
    unit=['[',unit2,'/',unit1,']'];
end

fig=figure;
  subplot(5,1,[1 2 3])
  loglog(freq,mag,'r-','LineWidth',2)
  grid on
  title(['Transfer Function Bode Plot',' from ',invl2,' to ',outvl],...
      'FontSize',12,'FontWeight','bold','FontName','Cambria')
  ylabel(['Magnitude ',unit],'FontSize',12,'FontWeight','bold','FontName','Cambria')
  set(gca,'FontSize',12,'FontName','Cambria')
  
  subplot(5,1,[4 5])
  semilogx(freq,phs,'r-','LineWidth',2)
  grid on
  ylim([-180 180])
  %xlim([10^(fmin) 10^(fmax)])
  ylabel('Phase [deg]','FontSize',12,'FontWeight','bold','FontName','Cambria')
  xlabel('Frequency (Hz)','FontSize',12,'FontWeight','bold','FontName','Cambria')
  set(gca,'FontSize',12,'FontName','Cambria')
  set(gca,'YTick',-180:90:180)

set(fig,'Position',[50, 50, 850, 650]);
  
end