function rms = makerms(x,y)
len=length(x);
sq=zeros(1,len);
rms=zeros(1,len);
for i=1:len
    if i==len
        sq(len-i+1)=sq(len-i+2);
    elseif i==1
        sq(len-i+1)=0;
    else
        sq(len-i+1)=sq(len-i+2)+y(len-i+1)^2*(x(len-i+1)-x(len-i));
    end
    rms(len-i+1)=sqrt(sq(len-i+1));
end
end
