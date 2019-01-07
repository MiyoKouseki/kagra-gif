function output_gain = mn_CMSgain(input_gain)

if input_gain>=0
    sign = '0';
    Din = input_gain;
else
    sign = '1';
    Din = input_gain+32;
end
bin_str = [sign dec2bin(abs(Din),5)];
bin = zeros(1,length(bin_str));
for ii = 1:length(bin_str)
    bin(ii) = not(str2double(bin_str(ii)));
end
Y = zeros(1,4);
if bin(1) == 0
    Y(1) = bin(2);
    Y(2) = bin(3);
    Y(3) = 1;
    Y(4) = 1;
else
    Y(1) = 0;
    Y(2) = 0;
    Y(3) = bin(2);
    Y(4) = bin(3);
end  

st_gain = zeros(1,8);
st_gain(1) = 1/(1+1.5);%-8dB
st_gain(2) = 0.620/(3.32+0.620);%-16dB
st_gain(3) = 1/(1+1.5);%-8dB
st_gain(4) = (3.32+0.620)/0.620;%16dB
st_gain(5) = (1+1.5)/1;%8dB
st_gain(6) = (2+1.2)/2;%4dB
st_gain(7) = (2+0.499)/2;%2dB
st_gain(8) = (3.32+0.374)/3.32;%1dB
st_gain_dB = log10(st_gain)*20;
SW_logic0 = [1 0 0 1 1 1 1 1];
SW_logic = [bin(1) Y bin(4:6)];
SW = zeros(1,length(SW_logic));
for ii = 1:length(SW)
    if SW_logic(ii) == 0
        SW(ii) = SW_logic0(ii);
    else
        SW(ii) = not(SW_logic0(ii));
    end
end

output_gain = SW*st_gain_dB';
end