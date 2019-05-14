function [mag,phs]=bodesus(sys,inv,outv,freq)

nin=strcmp(sys.InputName,inv);
nout=strcmp(sys.OutputName,outv);
[mag,phs] = mybode(sys(nout,nin),freq);

end