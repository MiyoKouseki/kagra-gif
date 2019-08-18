function tseek = dttxml_read_until(tbuf, tseek, find_name, verbose)
% read lines from fid until a line contains find_name found.

for tseek=tseek:length(tbuf)
    % check if we find the target line
    if isempty(strfind(tbuf{tseek}, find_name))
        %         % give some screen feedback every ten lines
        %         if verbose
        %             if mod(tseek,100)==0
        %                 fprintf(1,'*');
        %             end
        %             if mod(tseek,8000)==0
        %                 fprintf(1,'\n');
        %             end
        %         end
        
    else
        % yes we found
        if verbose
            fprintf(1,'\n');
            disp(['Found the end of the block']);
        end
        return
    end
    
end

if verbose
    disp('End of file reached.');
end


end