function dtt_sync = dttxml_parse_sync(header_buf)

dtt_sync = [];

dtt_sync = dttxml_parse_param(header_buf, dtt_sync, 'Start');

end
