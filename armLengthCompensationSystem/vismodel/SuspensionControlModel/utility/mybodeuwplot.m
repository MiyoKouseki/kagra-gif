function mybodeuwplot(sys,freq,varargin)

nsys=length(sys);
nmag=cell(nsys*2);
nphs=cell(nsys*2);

lgnd={};unit='';ttle='';
if nargin>2
    lgnd=varargin{1};
    if nargin>3
        ttle=varargin{2};
        if nargin>4
            unit=varargin{3};
        end
    end
end

for i=1:nsys
    nmag{i*2-1}=freq;nphs{i*2-1}=freq;
    [nmag{i*2},nphs{i*2}]=mybodeuw(sys{i},freq);
end

figure
  subplot(5,1,[1 2 3])
  loglog(nmag{1:nsys*2},'LineWidth',2)
  grid on
  title(ttle,...
      'FontSize',12,'FontWeight','bold','FontName','Cambria')
  ylabel(['Magnitude ',unit],'FontSize',12,'FontWeight','bold','FontName','Cambria')
  if ~isempty(lgnd)
  legend(lgnd{1:nsys});
  end
  set(gca,'FontSize',12,'FontName','Cambria')
  
  subplot(5,1,[4 5])
  semilogx(nphs{1:nsys*2},'LineWidth',2)
  grid on
  %ylim([-180 180])
  %xlim([10^(fmin) 10^(fmax)])
  ylabel('Phase [deg]','FontSize',12,'FontWeight','bold','FontName','Cambria')
  xlabel('Frequency (Hz)','FontSize',12,'FontWeight','bold','FontName','Cambria')
  set(gca,'FontSize',12,'FontName','Cambria')
  set(gca,'YTick',-1800:90:1800)
  
end

