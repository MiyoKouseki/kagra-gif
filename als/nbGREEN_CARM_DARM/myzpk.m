function filter=myzpk(freq,ZQ,PQ,g);
% returns TF of filter
% freq: frequencies in Hz (If freq='zpk', it return zpk function.)
% ZQ: matrix of zeros (and Qs)
% PQ: matrix of poles (and Qs)
% g: filter gain
% Autor: Yuta Michimura

if length(ZQ)==0;
    zeros=[];
    Qzeros=[];
else
    zeros=ZQ(:,1)*2*pi;
    try
        Qzeros=ZQ(:,2);
    end
end
if length(PQ)==0;
    poles=[];
    Qpoles=[];
else
    poles=PQ(:,1)*2*pi;
    try
        Qpoles=PQ(:,2);
    end
end
z=[];
p=[];
for kk=1:length(zeros);
    try
        a=1/(2*Qzeros(kk));
        b=sqrt(a^2-1);
        z=[z,-zeros(kk)*[a+b,a-b]];
        g=g/zeros(kk)^2;
    catch
        z=[z,-zeros(kk)];
        if zeros(kk)~=0;
            g=g/zeros(kk);
        else
            g=g/(2*pi);
        end
    end
end
for kk=1:length(poles);
    try
        a=1/(2*Qpoles(kk));
        b=sqrt(a^2-1);
        p=[p,-poles(kk)*[a+b,a-b]];
        g=g*poles(kk)^2;
    catch
        p=[p,-poles(kk)];
        if poles(kk)~=0;
            g=g*poles(kk);
        else
            g=g*(2*pi);
        end
    end
end

F=zpk(z,p,g);
if freq(1) ~= 'z';
    [Fgain,Fphase,omega]=bode(F,2*pi*freq);
    filter=squeeze(Fgain.*exp(i.*Fphase/180*pi));
else
    filter=F;
end