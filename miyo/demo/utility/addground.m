function sus=addground(sus,groundname)
% setground function registers the name of grounds

checkinput(sus,groundname); % error check

if ~isfield(sus,'g')
    sus.g.n={};
end

sus.g.n=[sus.g.n, groundname];

end



function checkinput(sus,groundname)
% input error check
if ~isstruct(sus)
    error('addground:InputError',...
        'First argument must be a structure with a name specified.')
end

if ~isfield(sus,'n')
    error('addground:InputError',...
        'First argument must be a structure with a name specified.')
end

if ~ischar(groundname)
    error('addground:InputError',...
        'Second argument must be a string.')
end

end