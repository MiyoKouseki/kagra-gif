function outFB = set_FB(gain, enable_FB_list )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
outFB = containers.Map;
outFB(['Gain']) = gain;
for ii = 1:10
    outFB([num2str(ii)]) = mnismember(enable_FB_list,ii);
end

end

