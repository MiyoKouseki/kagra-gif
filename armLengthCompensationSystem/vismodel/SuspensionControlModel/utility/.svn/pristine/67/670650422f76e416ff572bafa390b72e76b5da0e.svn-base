function ret = dttxml_seek_block(tbuf, tseek, find_name, verbose)

line_num = 1;

while 1
    % end of file detection
    if tseek == length(tbuf)+1
        if verbose
            fprintf(1,'\n');
            disp('End of file reached.');
        end
        
        ret = 0;
        return
    end
        
    % obtain one line
    line = tbuf{tseek};
    tseek = tseek + 1;
    line_num = line_num + 1;
    
    % check if we find the target line
    if isempty(regexp(line, ['<LIGO_LW.* Name=.*' find_name],'match'));
        
        % no we didn't find
        % give some screen feedback every ten lines
        if verbose
            if mod(line_num,10)==0
                %fprintf(1,'.');
            end
            if mod(line_num,800)==0
                %fprintf(1,'\n');
            end
        end
    else
        % yes we found
        if verbose
            fprintf(1,'\n');
            disp(['Found ' find_name ' block.']);
        end
        
        ret = tseek;
        return
    end
    
end