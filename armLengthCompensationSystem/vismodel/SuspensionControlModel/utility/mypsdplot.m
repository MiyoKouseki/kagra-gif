function mypsdplot(val,freq,varargin)

nsys=length(val);

lgnd={};unit='';ttle='';ps={};
if nargin>2
    lgnd=varargin{1};
    if nargin>3
        ttle=varargin{2};
        if nargin>4
            unit=varargin{3};
            if nargin>5
                ps=varargin{4};
            end
        end
    end
end

if isempty(ps)
nmag=cell(1,nsys*2);
for i=1:nsys
    nmag{2*i}=val{i};
    nmag{2*i-1}=freq;
end
else
nmag=cell(1,nsys*2);
for i=1:nsys
    nmag{3*i}  =ps{i};
    nmag{3*i-1}=val{i};
    nmag{3*i-2}=freq;
end
end

figure
  loglog(nmag{:},'LineWidth',2)
  grid on
  title(ttle,...
      'FontSize',12,'FontWeight','bold','FontName','Cambria')
  ylabel(['Magnitude ',unit],'FontSize',12,'FontWeight','bold','FontName','Cambria')
  if ~isempty(lgnd)
  legend(lgnd{1:nsys});
  end
  xlabel('Frequency (Hz)','FontSize',12,'FontWeight','bold','FontName','Cambria')
  set(gca,'FontSize',12,'FontName','Cambria')
  
end

