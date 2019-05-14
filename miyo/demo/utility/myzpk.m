function sys = myzpk(z1,p1,k1)
 sys=zpk(-z1*2*pi,-p1*2*pi,k1);
end