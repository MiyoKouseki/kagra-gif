function index = mnismember( list_arg, arg )
%UNTITLED23 Summary of this function goes here
%   Detailed explanation goes here
index = 0;
if iscell(list_arg)
    for ii = 1:length(list_arg)
        if ischar(list_arg{ii})
            if strcmp(list_arg{ii},arg)
                index = ii;
                break
            end
        else
            if isequal(list_arg{ii}, arg)
                index = ii;
                break
            end
        end
    end
else
    for ii = 1:length(list_arg)
        
        if ischar(list_arg(ii))
            
            if strcmp(list_arg(ii),arg)
                index = ii;
                break
            end
        else
            if isequal(list_arg(ii), arg)
                index = ii;
                break
            end
        end
    end
end
