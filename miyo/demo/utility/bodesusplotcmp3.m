function bodesusplotcmp3(sys1,inv1,outv1,inv2,outv2,inv3,outv3,freq,varargin)

nin1=strcmp(sys1.InputName,inv1);
nout1=strcmp(sys1.OutputName,outv1);
[mag1,phs1] = mybode(sys1(nout1,nin1),freq);

nin2=strcmp(sys1.InputName,inv2);
nout2=strcmp(sys1.OutputName,outv2);
[mag2,phs2] = mybode(sys1(nout2,nin2),freq);

nin3=strcmp(sys1.InputName,inv3);
nout3=strcmp(sys1.OutputName,outv3);
[mag3,phs3] = mybode(sys1(nout3,nin3),freq);

unit=makeunit(inv1,outv1);
leg={'data1','data2'};

if ~isempty(varargin)
if iscellstr(varargin{1})
    if length(varargin{1})>1
        leg=varargin{1};
    end
end
end

figure
  subplot(5,1,[1 2 3])
  loglog(freq,mag1,'k-',freq,mag2,'r-',freq,mag3,'b-','LineWidth',2)
  grid on
  title('Transfer Function Bode Plot',...
      'FontSize',12,'FontWeight','bold','FontName','Cambria')
  ylabel(['Magnitude ',unit],'FontSize',12,'FontWeight','bold','FontName','Cambria')
  legend(leg{1},leg{2},leg{3});
  set(gca,'FontSize',12,'FontName','Cambria')
  
  subplot(5,1,[4 5])
  semilogx(freq,phs1,'k-',freq,phs2,'r-',freq,phs3,'b-','LineWidth',2)
  grid on
  ylim([-180 180])
  %xlim([10^(fmin) 10^(fmax)])
  ylabel('Phase [deg]','FontSize',12,'FontWeight','bold','FontName','Cambria')
  xlabel('Frequency (Hz)','FontSize',12,'FontWeight','bold','FontName','Cambria')
  set(gca,'FontSize',12,'FontName','Cambria')
  set(gca,'YTick',-180:90:180)
  
end