function plotbode(freq,varargin);
% bodeplot for many TFs

Ntf=size(varargin{:},2);
tf=[varargin{:}];
try
    % when TFs are given as complex numbers
    subplot(2,1,1);
    loglog(freq,abs(tf));
    subplot(2,1,2);
    semilogx(freq,angle(tf)/pi*180);
catch
    % when Tfs are given as zpk functions
    [mag,ph]=bode(tf,2*pi*freq);
    for kk=1:Ntf
        subplot(2,1,1);
        loglog(freq,squeeze(mag(1,kk,:)));
        hold all;
        subplot(2,1,2);
        semilogx(freq,squeeze(angle(exp(i*ph(1,kk,:)/180*pi))/pi*180));
        hold all;
    end
end    
subplot(2,1,1);
ylabel('Gain');
grid on;
subplot(2,1,2);
xlabel('Frequency [Hz]');
ylabel('Phase [deg]');
grid on;
ylim([-180,180]);
set(gca,'YTick',linspace(-180,180,7));