function dtt_result = dttxml_parse_result(buf, verbose)

res = regexp(buf(1),'.*Name="(.*)".*Type="(.*)".*','tokens');

name = strrep(strrep(res{1}{1}{1},'[',''),']','');
dtt_result.Name = name;
dtt_result.Type = res{1}{1}{2};


if verbose
    disp(['Reading ' name ' data']);
end

for line_num = 1:length(buf)
    if ~isempty(strfind(buf{line_num},'<Stream'))
        first_line = line_num + 1;
        break
    end
end

buf_head = buf(1:first_line-1);

for param = {...
        'f0','df','t0','Subtype','dt','BW','Window',...
        'AverageType','Averages',...
        'N','M','Channel','ChannelA'...
        }
    
    dtt_result = dttxml_parse_param(buf_head, dtt_result, param{1});
end

dtt_result = dttxml_parse_param_list(buf_head, dtt_result, 'ChannelB');

for line_num = first_line:length(buf)
    
    % loop until the end of the stream block
    if ~isempty(strfind(buf{line_num},'</Stream'))
        % here is the termination process
        last_line = line_num - 1;
        break;
    end
    
    %     if verbose
    %         % give some screen feedback every ten lines
    %         if mod(line_num,100)==0
    %             fprintf(1,'.');
    %         end
    %         if mod(line_num,8000)==0
    %             fprintf(1,'\n');
    %         end
    %     end
    
end

line_buf = [buf{first_line:last_line}];
data_buf = base64decode(line_buf);
dtt_result.Data = double(typecast(data_buf, 'single'));

end