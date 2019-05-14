function sys = myresonantfilter(f,Q1,Q2)
  fc1=myfQ(f,Q1);
  fc2=myfQ(f,Q2);
  sys=myzpk(fc1,fc2,1);
end