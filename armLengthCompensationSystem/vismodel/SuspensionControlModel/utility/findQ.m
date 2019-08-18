function [f,Tdamp] = findQ(sys,finp,varargin)

if ~isempty(varargin)
    tol=varargin{1};
else
    tol=1e-3;
end

vecpole=pole(sys);
vecpole=vecpole(real(vecpole)<0);
vecpole=vecpole(imag(vecpole)>1e-6);
vecpolei=imag(vecpole)/2/pi;
vecpoler=-1./real(vecpole);
[vecpolei,numpolei]=sort(vecpolei);
vecpoler=vecpoler(numpolei);

nvp=length(vecpolei);
flg=false(1,nvp);

for i=1:nvp
    if abs(vecpolei(i)-finp)<tol
        flg(i)=true;
    end
end
f=vecpolei(flg);
Tdamp=vecpoler(flg);

disp([num2str(length(f)),' resonances are found:']);

for i=1:length(f)
    disp(['f=',num2str(f(i)),' Hz, Tdamp=',num2str(Tdamp(i)),'sec']);
end

end
