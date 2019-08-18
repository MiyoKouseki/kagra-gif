function hdr_out = dttxml_parse_param_list(cell_buf, hdr_in, find_name)

idx = regexp(cell_buf, ['<(\w+) Name="' find_name '\W\d+\W.*>(.*)</\1>'],'tokens');
idx = idx(~cellfun('isempty',idx));

list={};

if ~isempty(idx)
    for ii=1:length(idx)
        list=[list; idx{ii}{1}{2}];
    end
    
    hdr_in.(find_name)=list;
else
    hdr_in.(find_name)='';
end

hdr_out = hdr_in;

end