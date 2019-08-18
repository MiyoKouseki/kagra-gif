%% main
function bodesusplotopt(sys,inv,outv,freq,varargin)

nin=length(varargin);
% VARARGIN CHECK
if rem(nin,2)==1
   error('bodesusplotopt:InputError','Number of varargin must be even.')
end

% VARARGIN CHECK
fg_t=0; fg_y=0; fg_yl=0; fg_c=0; fg_p=0; fg_cb=0; fg_u1=0; fg_u2=0;
for n=1:nin/2
    if strcmp(varargin{2*n-1},'title')
        titlearg=varargin{2*n}; fg_t=1;
    end
    if strcmp(varargin{2*n-1},'ylim')
        ylimarg=varargin{2*n}; fg_y=1;
    end
    if strcmp(varargin{2*n-1},'ylabel')
        ylabelarg=varargin{2*n}; fg_yl=1;
    end
    if strcmp(varargin{2*n-1},'color')
        colorarg=varargin{2*n}; fg_c=1;
    end
    if strcmp(varargin{2*n-1},'position')
        positionarg=varargin{2*n}; fg_p=1;
    end
    if strcmp(varargin{2*n-1},'calibration')
        calib=varargin{2*n}; fg_cb=1;
    end
    if strcmp(varargin{2*n-1},'unit1')
        unit1=varargin{2*n}; fg_u1=1;
    end
    if strcmp(varargin{2*n-1},'unit2')
        unit2=varargin{2*n}; fg_u2=1;
    end
end


% FIND INPUT/OUTPUT VARIABLES
nin=strcmp(sys.InputName,inv);
nout=strcmp(sys.OutputName,outv);
if isempty(nin)||isempty(nout)
    error('bodesusplotopt:InputError','No input/output name found.')
end

% UNIT CHECK
if ~fg_u1; unit1=unittake(inv); end;
if ~fg_u2; unit2=unittake(outv); end;
if  strcmp(unit1,'1')||strcmp(unit2,'1'); unit='';
else unit=['[',unit2,'/',unit1,']']; end

% VARARGIN SET
if ~fg_c; colorarg='r-'; end;
if ~fg_t; titlearg=['Transfer Function Bode Plot',' from ',inv,' to ',outv];end;
if ~fg_yl; ylabelarg=['Magnitude ',unit]; end;
if ~fg_p; positionarg=[50, 50, 850, 650]; end;
if ~fg_cb; calib=1; end;

% TRANSFER FUNCTION
[mag,phs] = mybode(sys(nout,nin)*calib,freq);

fig=figure;
subplot(5,1,[1 2 3])
loglog(freq,mag,colorarg,'LineWidth',2)
grid on
title(titlearg,'FontSize',12,'FontWeight','bold','FontName','Times New Roman',...
    'interpreter','none')
ylabel(ylabelarg,'FontSize',12,'FontWeight','bold','FontName','Times New Roman')
set(gca,'FontSize',12,'FontName','Times New Roman')
if fg_y; ylim(ylimarg); end;
  
subplot(5,1,[4 5])
semilogx(freq,phs,colorarg,'LineWidth',2)
grid on
ylim([-180 180])
ylabel('Phase [deg]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
xlabel('Frequency [Hz]','FontSize',12,'FontWeight','bold','FontName','Times New Roman')
set(gca,'FontSize',12,'FontName','Times New Roman')
set(gca,'YTick',-180:90:180)
set(fig,'Position', positionarg)
set(fig,'Color','white')
  
end



%% unittake
function unit=unittake(inv)

if strncmp(inv,'L',1)||strncmp(inv,'T',1)||strncmp(inv,'V',1)
    unit='m';
elseif strncmp(inv,'R',1)||strncmp(inv,'P',1)||strncmp(inv,'Y',1)
    unit='rad';
elseif strncmp(inv,'actL',4)||strncmp(inv,'actT',4)||strncmp(inv,'actV',4)
    unit='N';
elseif strncmp(inv,'actR',4)||strncmp(inv,'actP',4)||strncmp(inv,'actY',4)
    unit='Nm';
elseif strncmp(inv,'LVDT_L',6)||strncmp(inv,'LVDT_T',6)||strncmp(inv,'LVDT_V',6)
    unit='m';
elseif strncmp(inv,'LVDT_Y',6)
    unit='rad';
elseif strncmp(inv,'OSEM_L',6)||strncmp(inv,'OSEM_T',6)||strncmp(inv,'OSEM_V',6)
    unit='m';
elseif strncmp(inv,'OSEM_R',6)||strncmp(inv,'OSEM_P',6)||strncmp(inv,'OSEM_Y',6)
    unit='rad';
elseif strncmp(inv,'OpLev',5)
    unit='rad';
elseif strncmp(inv,'IFO_L',5)
    unit='m';
elseif strncmp(inv,'velL',4)||strncmp(inv,'velT',4)||strncmp(inv,'velV',4)
    unit='(m/s)';
elseif strncmp(inv,'velR',4)||strncmp(inv,'velP',4)||strncmp(inv,'velY',4)
    unit='(rad/s)';
elseif strncmp(inv,'GEO_L',5)||strncmp(inv,'GEO_T',5)||strncmp(inv,'GEO_V',5)
    unit='(m/s)';
elseif strncmp(inv,'GEO_P',5)||strncmp(inv,'GEO_R',5)||strncmp(inv,'GEO_Y',5)
    unit='(rad/s)';
else
    unit='1';
end


end