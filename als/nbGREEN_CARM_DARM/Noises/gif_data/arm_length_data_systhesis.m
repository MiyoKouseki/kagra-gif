%%
clear all
close all
%%
gif = load('asd_diff_gif_.dat');
seis = load('asd_diff_seis_.dat');

one_point = load('../KamiokaSeismicHighNoise.txt');


%%

freq = gif(:,1);

one_point_interp = interp1(one_point(:,1),one_point(:,2),freq);

arm_length = (gif(:,2)*sqrt(2) .* (freq<=0.3) + seis(:,2)*sqrt(2) .* (freq>0.3) .* (freq<=0.7) + one_point_interp*sqrt(2) .* (freq>0.7)*1e6) /1e6 ;




%% plot to check the data
figure(1)

loglog(freq,arm_length,'r','LineWidth',5)
hold on
loglog(freq,gif(:,2)*sqrt(2)/1e6,'g')
hold on
loglog(freq,seis(:,2)*sqrt(2)/1e6,'y')
hold on
loglog(freq,one_point_interp*sqrt(2),'b')
grid on

xlabel('Frequency [Hz]')
ylabel('ASD [m/sqrt(Hz)]')

%% save data
data1(:,1)=freq;
data1(:,2)=arm_length;

filename='../KamiokaSeismicNoise_ArmLength.txt';
fileID = fopen(filename,'w');
fprintf(fileID,'%6.10f %12.30f \r\n',data1');
fclose(fileID);
clear data1



