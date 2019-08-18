function hdr_out = dttxml_parse_param(cell_buf, hdr_in, find_name)

%idx = regexp(cell_buf, ['<(\w+) Name="' find_name '.*>([\w:\-_\.]*).*</\1>'],'tokens');
idx = regexp(cell_buf, ['<(\w+) Name="' find_name '.*>(.*)</\1>'],'tokens');
idx = idx(~cellfun('isempty',idx));

if ~isempty(idx)
    hdr_in.(find_name)=idx{1}{1}{2};
else
    hdr_in.(find_name)='';
end

hdr_out = hdr_in;

end