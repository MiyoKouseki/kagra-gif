function sumdata = sumpsd(data)
if ~iscell(data); error('Input argument: {data1, data2, ...}'); end
len=length(data);
if ~isvector(data{1}); error('Input argument: {data1, data2, ...}'); end
dlen=length(data{1});
for i=2:len
    if length(data{i})~=dlen; error('Data lengths must be the same.'); end
end
sumdata=data{1}*0;
for i=1:len
    sumdata=sumdata+data{i}.^2;
end
sumdata=sqrt(sumdata);
end
