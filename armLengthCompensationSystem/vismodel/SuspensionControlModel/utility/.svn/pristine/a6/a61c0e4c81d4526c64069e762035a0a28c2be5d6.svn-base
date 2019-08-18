function result_name = dttxml_get_reference_result_name(refChCell,dtt_result)
    result_name = [];
    try
        channelAndReferenceNum = ...
            cellfun(...
            @(chanName)...
            regexp(chanName,...
            '(?<chan>.*)\(REF(?<result_num>[0-9]+)\)',...
            'tokens'),...
            refChCell);%,'UniformOutput',false);
    catch err
        if strcmp(err.identifier,'MATLAB:cellfun:NotAScalarOutput')
            % channels aren't references
            return
        end
    end
    
    refNums = cellfun(@(cell)str2double(cell{1,2}),channelAndReferenceNum);
    userChans = cellfun(@(cell)cell{1,1},channelAndReferenceNum,'UniformOutput',false);
    
    if ~all(refNums==refNums(1))
        error('Reference numbers must match for all channels')
    end
    
    result_name = ['Reference' num2str(refNums(1))];
    
    % check if result is even in the dtt_result struct
    try
        result = dtt_result.(result_name);
    catch err
        if strcmp(err.identifier,'MATLAB:nonExistentField')
            error([result_name ' doesn''t exist'])
        else
            err.rethrow()
        end
    end
    
    dttChans = [{result.Channel} {result.ChannelA} result.ChannelB];
    
    if ~strcmp(dttChans{1},userChans{1})
        error('Reference Channel A doesn''t match')
    end
    
    for jj = 2:length(userChans)
        if ~any(cellfun(@(chan)strcmp(chan,userChans{jj}),dttChans))
            error('Channel does not exist in result.')
        end
    end
    
end