function dtt_index = dttxml_parse_index(buf)

dtt_index = [];

str_buf='';

for ii=1:length(buf)
    str_buf=[str_buf buf{ii}];
end

delim = '</Param>';
buf=strsplit(str_buf,delim);

buf2 = {};
for ii=1:length(buf)
    buf2 =[buf2; [buf{ii} delim]];
end

% First part: Ignore

% Second part: MasterIndex
res=regexp(buf2{2},'.*>(.*)<.*','tokens');
idx=strsplit(res{1}{1},{':',';'});
res=regexp(idx,'.*Entry.* = (\w+).*','tokens');


dtt_index.MasterIndex={};

for ii=1:length(res)
    if ~isempty(res{ii})
        dtt_index.MasterIndex = [dtt_index.MasterIndex; res{ii}{1}{1}];
    end
end

% The rest: each entry
for ii=2:length(dtt_index.MasterIndex)
    if strcmp(dtt_index.MasterIndex{ii}, 'PowerSpectrum')
        % preparation
        res=regexp(buf2{ii+1},'.*>(.*)<.*','tokens');
        idx=strsplit(res{1}{1},';');
        
        % parameter extraction
        
        res=regexp(idx,'.*Channel.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Channel = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Name.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Name = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Length.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Length = cellfun(@(x) str2num(x{1}{1}), res);
        
        res=regexp(idx,'.*Offset.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Offset = cellfun(@(x) str2num(x{1}{1}), res);
    end
    
    if strcmp(dtt_index.MasterIndex{ii}, 'CrossCorrelation')||strcmp(dtt_index.MasterIndex{ii}, 'Coherence')
        % preparation
        res=regexp(buf2{ii+1},'.*>(.*)<.*','tokens');
        idx=strsplit(res{1}{1},';');
        
        % parameter extraction
        
        res=regexp(idx,'.*ChannelA.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).ChannelA = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*ChannelB.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).ChannelB = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Name.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Name = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Length.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Length = cellfun(@(x) str2num(x{1}{1}), res);
        
        res=regexp(idx,'.*Offset.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Offset = cellfun(@(x) str2num(x{1}{1}), res);
        
        dtt_index.(dtt_index.MasterIndex{ii}).Channel = [...
            dtt_index.(dtt_index.MasterIndex{ii}).ChannelA ...
            dtt_index.(dtt_index.MasterIndex{ii}).ChannelB ...
            ];
        
    end
    
    if strcmp(dtt_index.MasterIndex{ii}, 'TransferFunction')
        % preparation
        res=regexp(buf2{ii+1},'.*>(.*)<.*','tokens');
        idx=strsplit(res{1}{1},';');
        
        % parameter extraction
        res=regexp(idx,'.*ChannelA.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).ChannelA = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*ChannelB.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).ChannelB = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Name.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Name = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Length.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Length = cellfun(@(x) str2num(x{1}{1}), res);
        
        res=regexp(idx,'.*Offset.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Offset = cellfun(@(x) str2num(x{1}{1}), res);
        
        %disp(num2str(ii));
        
        dtt_index.(dtt_index.MasterIndex{ii}).Channel = [...
            dtt_index.(dtt_index.MasterIndex{ii}).ChannelA,...
            dtt_index.(dtt_index.MasterIndex{ii}).ChannelB...
            ];
    end
    
    if strcmp(dtt_index.MasterIndex{ii}, 'CoherenceFunction')
        % preparation
        res=regexp(buf2{ii+1},'.*>(.*)<.*','tokens');
        idx=strsplit(res{1}{1},';');
        
        % parameter extraction
        res=regexp(idx,'.*ChannelA.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).ChannelA = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*ChannelB.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).ChannelB = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Name.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Name = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Length.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Length = cellfun(@(x) str2num(x{1}{1}), res);
        
        res=regexp(idx,'.*Offset.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Offset = cellfun(@(x) str2num(x{1}{1}), res);
        
        dtt_index.(dtt_index.MasterIndex{ii}).Channel = [...
            dtt_index.(dtt_index.MasterIndex{ii}).ChannelA,...
            dtt_index.(dtt_index.MasterIndex{ii}).ChannelB...
            ];
    end
    
    if strcmp(dtt_index.MasterIndex{ii}, 'TimeSeries')
        % preparation
        res=regexp(buf2{ii+1},'.*>(.*)<.*','tokens');
        idx=strsplit(res{1}{1},';');
        
        % parameter extraction
        res=regexp(idx,'.*Channel.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Channel = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Name.* = (.*)','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Name = cellfun(@(x) x{1}, res);
        
        res=regexp(idx,'.*Length.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Length = cellfun(@(x) str2num(x{1}{1}), res);
        
        res=regexp(idx,'.*Offset.* = (\d+).*','tokens');
        res = res(~cellfun('isempty',res));
        dtt_index.(dtt_index.MasterIndex{ii}).Offset = cellfun(@(x) str2num(x{1}{1}), res);
        
    end
    
end

end