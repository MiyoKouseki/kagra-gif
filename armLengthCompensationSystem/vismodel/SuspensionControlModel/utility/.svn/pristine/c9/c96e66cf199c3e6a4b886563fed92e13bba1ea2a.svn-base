function pimp=makeeigenlist(sus,varargin)

stv=sus.m.stv;
ns=length(stv);
matM=sus.m.matM(1:ns,1:ns);
matK=real(sus.m.matK(1:ns,1:ns));

thr=0.2;
if ~isempty(varargin)
    if isreal(varargin{1})
        thr=varargin{1};
    end
end

[evec,evalmat]=eig(matM\matK);
eval=diag(evalmat);
efreq=sqrt(eval)/2/pi;
[efreq,esrt]=sort(efreq);
evec=evec(:,esrt);
pimp=cell(ns,ns+2);

for n=1:ns
    nimp=find(abs(evec(:,n))>thr);
    vimp=stv(nimp);
    eimp=evec(nimp,n);
    pimp{n,1}=num2str(n);
    pimp{n,2}=['f=',num2str(efreq(n),3),' Hz'];
    for m=1:length(nimp)
    pimp{n,m+2}=[vimp{m},'(',num2str(eimp(m),3),')'];
    end
end

%print(pimp);

end
