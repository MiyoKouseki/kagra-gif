function rms=plotspectrumRMS2(freq,spe,clr);
% plot cumulative RMS for a spectrum
% returns RMS

Nfreq=length(freq);
cumulativeRMS=[];
cumulativeRMSsquared=zeros(1,Nfreq);
for k=(Nfreq-1):-1:1
    if isnan(spe(k)) | isnan(spe(k+1))
        continue;
    end
    cumulativeRMSsquared(k)=cumulativeRMSsquared(k+1)+(spe(k+1)^2+spe(k)^2)*(freq(k+1)-freq(k))/2;
end
	cumulativeRMS=[cumulativeRMS;sqrt(cumulativeRMSsquared)];

rms=cumulativeRMS(:,1);
loglog(freq,cumulativeRMS,':','Color',clr);
text(freq(1),rms*10,['RMS = ',num2str(rms,'%.3f')],'Color',clr);