function sysp=takesusonly(sys,inv,outv)

nin=strcmp(sys.InputName,inv);
nout=strcmp(sys.OutputName,outv);
% sysp = minreal(sys(nout,nin));
sysp = sys(nout,nin);

end