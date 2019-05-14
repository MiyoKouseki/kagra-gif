function [mag,phs] = mybodeuw(sys,freqVec)
  [mag,phs1] = bode(sys,freqVec*(2*pi));
  mag = squeeze(mag)';
  phs1= squeeze(phs1)';
  phs = phs1;
  %abs = exp(1i*phs1*pi/180);
  %phs = angle(abs)*180/pi;
end