function dtt_test = dttxml_parse_test(buf)

dtt_test = [];

dtt_test = dttxml_parse_param(buf, dtt_test, 'StartFrequency');
dtt_test = dttxml_parse_param(buf, dtt_test, 'StopFrequency');
dtt_test = dttxml_parse_param(buf, dtt_test, 'NumberOfPoints');
dtt_test = dttxml_parse_param(buf, dtt_test, 'BW');
dtt_test = dttxml_parse_param(buf, dtt_test, 'Overlap');
dtt_test = dttxml_parse_param(buf, dtt_test, 'Window');
dtt_test = dttxml_parse_param(buf, dtt_test, 'AChannels');
dtt_test = dttxml_parse_param(buf, dtt_test, 'AverageType');
dtt_test = dttxml_parse_param(buf, dtt_test, 'Averages');
dtt_test = dttxml_parse_param(buf, dtt_test, 'SettlingTime');
dtt_test = dttxml_parse_param(buf, dtt_test, 'StimulusAmplitude');
dtt_test = dttxml_parse_param(buf, dtt_test, 'StimulusChannel');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusType');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusFrequency');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusAmplitude');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusOffset');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusPhase');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusRatio');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusFrequencyRange');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusAmplitudeRange');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'MeasurementChannel');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'MeasurementActive');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusChannel');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusActive');
dtt_test = dttxml_parse_param_list(buf, dtt_test, 'StimulusReadback');

end
