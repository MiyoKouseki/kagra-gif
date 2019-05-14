function cf = myfQv(f,Q)
cf=[f/2/Q+1i*f*sqrt(1-(1/2/Q)^2);f/2/Q-1i*f*sqrt(1-(1/2/Q)^2)];
end