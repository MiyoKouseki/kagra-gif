function sysp=takesysname(sys,inv,outv)

nin=strcmp(sys.InputName,inv);
nout=strcmp(sys.OutputName,outv);
sysp= sys(nout,nin);

end