function sys = mycheby2(n,R,f)
  [z,p,k]=cheby2(n,R,f*2*pi,'s');
  sys = zpk(z,p,k);
end