function bodesusplot(sys,inv,outv,freq)

nin=strcmp(sys.InputName,inv);
nout=strcmp(sys.OutputName,outv);
[mag,phs] = mybode(sys(nout,nin),freq);

if strncmp(inv,'L',1)||strncmp(inv,'T',1)||strncmp(inv,'V',1)
    unit1='m';
elseif strncmp(inv,'R',1)||strncmp(inv,'P',1)||strncmp(inv,'Y',1)
    unit1='rad';
elseif strncmp(inv,'actL',1)||strncmp(inv,'actT',1)||strncmp(inv,'actV',1)
    unit1='N';
elseif strncmp(inv,'actR',1)||strncmp(inv,'actP',1)||strncmp(inv,'actY',1)
    unit1='Nm';
else
    unit1='1';
end

if strncmp(outv,'L',1)||strncmp(outv,'T',1)||strncmp(outv,'V',1)
    unit2='m';
elseif strncmp(outv,'R',1)||strncmp(outv,'P',1)||strncmp(outv,'Y',1)
    unit2='rad';
elseif strncmp(outv,'senL',1)||strncmp(outv,'senT',1)||strncmp(outv,'senV',1)
    unit2='m';
elseif strncmp(outv,'senR',1)||strncmp(outv,'senP',1)||strncmp(outv,'senY',1)
    unit2='rad';
elseif strncmp(outv,'velL',1)||strncmp(outv,'velT',1)||strncmp(outv,'velV',1)
    unit2='(m/s)';
elseif strncmp(outv,'velR',1)||strncmp(outv,'velP',1)||strncmp(outv,'velY',1)
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
  title(['Transfer Function Bode Plot',' from ',inv,' to ',outv],...
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