function [ch_i, ch_len] = dttxml_prepare_chan(chAB,testName,dtt_index,ch_name)
    chA_list = strcmp(dtt_index.(testName).(['Channel' chAB]),ch_name);
    ch_i = find(chA_list,1);
    ch_len = length(chA_list);
end