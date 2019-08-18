function sus = makesusstructure(modelname)
% makesusstructure function makes a structure system
% with a name specified with the input argnment

checkinput(modelname); % error check
sus = struct('n',modelname);

end

function checkinput(modelname)
% input error check
if ~ischar(modelname)
    error('makesusstrcture:InputError',...
          'First argument must be a string.')
end
end