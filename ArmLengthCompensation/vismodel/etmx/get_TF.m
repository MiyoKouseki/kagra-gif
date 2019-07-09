clear all
close all
addpath /users/VIS/TypeBp/utility

%%
freq = linspace(1e-2, 1e2, 10001);

gain_dc = 0.01452/0.0126;

gain = [gain_dc 0.03125 0];
p0 = [0.445 80 -1];
p1 = [0.726 100 -1];
p2 = [0.8514 45 -1];
p3 = [0.968 30 -1];
p4 = [1.029 70 -1];
p5 = [1.365 20 -1];
p6 = [1.27 20 -1];
p7 = [0.077 8 -1];
p8 = [0.218 25 -1];

z0 = [0.156 25 1];
z1 = [0.398 100 1];
z2 = [0.687 100 1];
z3 = [0.843 40 1];
z4 = [0.955 30 1];
z5 = [1.0162 80 1];
z6 = [1.35 30 1];
z7 = [1.258 25 1];
z8 = [7 8 1];

fq = [gain; p0; p1; p2; p3; p4; p5; p6; p7; p8; z0; z1; z2; z3; z4; z5; z6; z7;z8];
fit = fqtf(freq, fq).';
close all;
figure;

subplot(2,1,1);
loglog(freq, abs(fit));
grid;
legend({'model'},'Location','southwest');

subplot(2,1,2);
semilogx(freq, angle(fit)*180/pi);
grid;

saveas(gcf,'TF_ETMX_GNDtoIPL_disp_model.pdf');

mag = abs(fit);
phs = angle(fit)*180/pi;

TF = [freq; mag.'; phs.'];

fileID = fopen('tfmodel.txt','w');
fprintf(fileID,'# %s\n','frequency[Hz], mag, phase[deg]');
fprintf(fileID,'%.5e %.5e %.5e \n',TF);
fclose(fileID);

