function sus=makestatespacemodel(sus)

% buildsusmodel

sanitycheck(sus);

inv=sus.m.inv;
stv=sus.m.stv;
ni=length(inv);
ns=length(stv);

matM=sus.m.matM(1:ns,1:ns);
matG=sus.m.matG(1:ns,1:ns);
matK=sus.m.matK(1:ns,1:ns);
matK0=sus.m.matK(1:ns,ns+1:ns+ni);

stvv=stv;
stvf=stv;
for n=1:ns
    stvv{n}=['vel',stv{n}];
    stvf{n}=['act',stv{n}];
end
invar=[inv,stvf];
stvar=[stvv,stv];

matA=[-matM\matG,-matM\real(matK);
    eye(ns),zeros(ns,ns)];
matB=[-matM\real(matK0),matM\eye(ns);
    zeros(ns,ni),zeros(ns,ns)];
matC=eye(2*ns);
matD=zeros(2*ns,ns+ni);
smdlss=ss(matA,matB,matC,matD,'statename',stvar,'inputname',invar,'outputname',stvar);

sus.ss=smdlss;


end






% SANITY CHECK
function sanitycheck(smdl)

if ~isstruct(smdl)
error('MyFunc:InputError','First input should be a structure.')
end

end




