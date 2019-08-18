classdef DttData
    
    properties
        rawDataStruct = struct();
        channels;
        verbose;
    end
    
    methods
        
        function objOut = DttData(input, varargin)
            
            if any(strcmp('verbose',varargin))
                verbose = 1;
            else
                verbose = 0;
            end
            
            % constructor
            
            % if it's a string, try to read the file
            if ischar(input)
                objOut = DttData.readDttXml(input, verbose);
                return
            end
            
            % else, it's already been read
            data = input;
            
            objOut.rawDataStruct = data;
            objOut.channels = data.dtt_index.(data.dtt_index.MasterIndex{2}).Channel;
        end
        
        function [t,data] = timeSeries(dttObj,chanName)
            
            dtt_index = dttObj.rawDataStruct.dtt_index;
            dtt_result = dttObj.rawDataStruct.dtt_result;
            dtt_header = dttObj.rawDataStruct.dtt_header;
            
            % check if it's a reference
            % this returns {} if it is not a reference
            result_name = dttxml_get_reference_result_name({chanName},dtt_result);
            
            if isempty(result_name)
                % the case that a reference is not requested
                
                % prepare A ch
                
                if ~strcmp(dtt_header.TestType,'TimeSeries')
                    error('Measurement type is not time series')
                end
                
                chanIndex = find(strcmp(chanName,dtt_index.TimeSeries.Channel),1);
                
                if isempty(chanIndex)
                    error('Channel is not found.')
                end
                
                result_name = ['Result' num2str(chanIndex-1)];
            end
            
            %disp(resultName)
            
            result = dtt_result.(result_name);
            
            N = str2num(result.N);
            dt = str2num(result.dt);
            
            t = dt:dt:dt*N;
            data = result.Data;
            
            % if there's only one output argument, make a timeseries object
            if nargout == 1
                t = timeseries(data,t,'name',chanName);
                t.DataInfo.Units = 'counts';
                t.TimeInfo.Units = 'seconds';
                %t.TimeInfo.Format = 'SS';
                %t.TimeInfo.StartDate = dtt_header.TestTimeUTC;
            end
        end
        
        function [freq, tf_cmplx] = transferFunction(dttObj,chA_name,chB_name)
            switch dttObj.rawDataStruct.dtt_header.TestType
                case 'SweptSine'
                    [freq, tf_cmplx] = transferFunctionSweptSine(dttObj,chA_name,chB_name);
                case 'FFT'
                    [freq, tf_cmplx] = transferFunctionFft(dttObj,chA_name,chB_name);
                otherwise
                    disp('Could not find appropriate measurement type!');
                    freq =[];
                    tf_cmplx = [];
            end
            
            if nargout == 1
                % there is a single output, let's make it an frd object
                freq = frd(tf_cmplx(freq~=0),freq(freq~=0),'FrequencyUnit','Hz');
            end
        end
        
        function [freq, tf_cmplx] = transferFunctionSweptSine(dttObj,chA_name,chB_name)
            
            dtt_index = dttObj.rawDataStruct.dtt_index;
            dtt_result = dttObj.rawDataStruct.dtt_result;
            
            % check if it's a reference
            % this returns {} if it is not a reference
            result_name = dttxml_get_reference_result_name({chA_name,chB_name},dtt_result);
            chB_i = 1;
            
            if isempty(result_name)
                % the case that a reference is not requested
                
                % prepare channels
                testName = 'TransferFunction';
                [chA_i,chA_len] = dttxml_prepare_chan('A',testName,dtt_index,chA_name);
                [chB_i,~] = dttxml_prepare_chan('B',testName,dtt_index,chB_name);
                if isempty(chA_i)
                    error('Requested A channel not found!');
                end
                
                if isempty(chB_i)
                    error('Requested B channel not found!');
                end
                
                % note
                
                if strcmp(chA_name, chB_name)
                    disp('Warning:');
                    disp('When the given two channels are the same,');
                    disp('dtt2tf returns the amplitude response of the channel');
                    disp('instead of the the transfer function of the unity.');
                    disp('Maybe.');
                end
                
                % DEBUG
                % chA_len = length(chA_list);
                
                % prepare B ch
                
                res_list = dtt_index.TransferFunction.Name;
                
                result_name = strrep(strrep(res_list{chA_i*chA_len},'[',''),']','');
            end
            data = dtt_result.(result_name);
            
            % DEBUG
            % chB_len = length(chB_list);
            
            %% Transfer Function
            
            % extract data block
            tf_data = data.Data;
            
            % # of frequency bins
            n  = str2double(data.N);
            
            % data total size
            tf_data_sz = size(tf_data);
            
            % convert to complex numbers
            tf_data_reshaped = reshape(tf_data, 2, tf_data_sz(2)/2);
            tf_data_reshaped_cmplx = tf_data_reshaped(1,:)+1i*tf_data_reshaped(2,:);
            
            % first N data is the frequency list
            freq = tf_data_reshaped_cmplx(1:n);
            
            % The rest is the TF data
            tf_data_reshaped_cmplx = tf_data_reshaped_cmplx(n+1:end);
            
            % cut out the requested part
            tf_cmplx = tf_data_reshaped_cmplx((n*(chB_i-1)+1):(n*(chB_i)));
            
            freq = transpose(freq);
            tf_cmplx = transpose(tf_cmplx);
        end
        
        function [freq, tf_cmplx] = transferFunctionFft(dttObj,chA_name,chB_name)
            
            dtt_index = dttObj.rawDataStruct.dtt_index;
            dtt_result = dttObj.rawDataStruct.dtt_result;
            
            % check if it's a reference
            % this returns {} if it is not a reference
            result_name = dttxml_get_reference_result_name({chA_name,chB_name},dtt_result);
            chB_i = 1;
            
            % get_refereence_result_name returns empty array if it's not a
            % reference channel
            if isempty(result_name)
                % the case that a reference is not requested
                
                % prepare A ch
                testName = 'CrossCorrelation';
                [chA_i,~] = dttxml_prepare_chan('A',testName,dtt_index,chA_name);
                
                if isempty(chA_i)
                    error('Requested A channel not found!');
                end
                
                chB_len = sum(strcmp(dttObj.rawDataStruct.dtt_test.MeasurementActive,'true'));
                
                % prepare B ch
                
                %                 res_list = dtt_index.CrossCorrelation.Name;
                
                %                 result_name = strrep(strrep(res_list{(chA_i-1)*(chB_len-1)+1},'[',''),']','');
                %                 data = dtt_result.(result_name);
                %
                %                 chB_list = strcmp(data.ChannelB,chB_name);
                %                 chB_i = find(chB_list,1);
                %
                %                 if isempty(chB_i)
                %                     error('Requested B channel not found!');
                %                 end
                
                res_list = unique(dtt_index.CrossCorrelation.Name);
                
                for res_i=1:length(res_list) % scan for all results
                    
                    result_name = strrep(strrep(res_list{res_i},'[',''),']','');
                    data = dtt_result.(result_name);
                    % DEBUG
                    % disp([num2str(res_i) ': ' data.ChannelA ' : ' chA_name]);
                    
                    if strcmp(data.ChannelA,chA_name)
                        chB_list = strcmp(data.ChannelB,chB_name);
                        chB_i = find(chB_list,1);
                        
                        if isempty(chB_i)
                            error(['Requested B channel not found in ' result_name]);
                        else
                            % DEBUG
                            % disp(['Found ' chB_name ' in ' result_name]);
                            break
                        end
                    end
                end
                
                %{chA_i chB_i result_name chA_name chB_name}
                %dttObj.dtt_result.(result_name).ChannelB
                
                % DEBUG
                % chB_len = length(chB_list);
                
                %% Cross spectrum P_AB
                
                % extract data block
                corr_data = data.Data;
                
                % frequency bins
                f0 = str2double(data.f0);
                n  = str2double(data.N);
                df = str2double(data.df);
                
                freq = f0+(0:n-1)*df;
                
                % data total size
                corr_data_sz = size(corr_data);
                
                % convert to complex numbers
                corr_data_reshaped = reshape(corr_data, 2, corr_data_sz(2)/2);
                corr_data_reshaped_cmplx = corr_data_reshaped(1,:)+1i*corr_data_reshaped(2,:);
                
                % cut out the requested part
                cross_spe = corr_data_reshaped_cmplx((n*(chB_i-1)+1):(n*(chB_i)));
                
                %% Power spectrum sqrt(P_AA)
                
                [freq_tmp psd] = powerSpectrum(dttObj, chA_name);
                
                %% Transfer function: P_BA/P_AA = conj(P_AB)/sqrt(P_AA)^2
                tf_cmplx = conj(cross_spe)./psd.^2;
                
            else
                data = dtt_result.(result_name);
                
                % extract data block
                tf_data = data.Data;
                
                % frequency bins
                f0 = str2double(data.f0);
                n  = str2double(data.N);
                df = str2double(data.df);
                
                freq = f0+(0:n-1)*df;
                
                % data total size
                tf_data_sz = size(tf_data);
                
                % convert to complex numbers
                tf_data_reshaped = reshape(tf_data, 2, tf_data_sz(2)/2);
                tf_data_reshaped_cmplx = tf_data_reshaped(1,:)+1i*tf_data_reshaped(2,:);
                
                tf_cmplx = tf_data_reshaped_cmplx;
                
            end
            
            % common part for a result data and a reference data
            
            freq = transpose(freq);
            tf_cmplx = transpose(tf_cmplx);
        end
        
        function [freq, coh] = coherence(dttObj, chA_name, chB_name)
            
            switch dttObj.rawDataStruct.dtt_header.TestType
                case 'SweptSine'
                    [freq, coh] = coherenceSweptSine(dttObj, chA_name, chB_name);
                case 'FFT'
                    [freq, coh] = coherenceFft(dttObj, chA_name, chB_name);
                otherwise
                    disp('Could not find appropriate measurement type!');
                    freq =[];
                    coh = [];
            end
            
        end
        
        function [freq, coh] = coherenceSweptSine(dttObj,chA_name,chB_name)
            
            dtt_index = dttObj.rawDataStruct.dtt_index;
            dtt_result = dttObj.rawDataStruct.dtt_result;
            
            % check if it's a reference
            % this returns {} if it is not a reference
            result_name = dttxml_get_reference_result_name({chA_name,chB_name},dtt_result);
            chB_i = 1;
            
            if isempty(result_name)
                % the case that a reference is not requested
                
                % prepare A ch
                testName = 'TransferFunction';
                [chA_i,chA_len] = dttxml_prepare_chan('A',testName,dtt_index,chA_name);
                [chB_i,~] = dttxml_prepare_chan('B',testName,dtt_index,chB_name);
                
                if isempty(chA_i)
                    disp('Requested A channel not found!');
                    freq =[];
                    tf_cmplx = [];
                    return
                end
                
                if isempty(chB_i)
                    disp('Requested B channel not found!');
                    freq =[];
                    tf_cmplx = [];
                    return
                end
                
                % prepare B ch
                res_list = dtt_index.CoherenceFunction.Name;
                
                result_name = strrep(strrep(res_list{chA_i*chA_len},'[',''),']','');
            end
            data = dtt_result.(result_name);
            
            %% Coherence Function
            
            % extract data block
            coh_data = data.Data;
            
            % # of frequency bins
            n  = str2double(data.N);
            
            % first N data is the frequency list
            freq = coh_data(1:n);
            
            % The rest is the coherence data
            coh_data = coh_data(n+1:end);
            
            % cut out the requested part
            coh = coh_data((n*(chB_i-1)+1):(n*(chB_i)));
            
            freq = transpose(freq);
            coh = transpose(coh);
        end
        
        function [freq, coh] = coherenceFft(dttObj, chA_name, chB_name)
            
            dtt_index = dttObj.rawDataStruct.dtt_index;
            dtt_result = dttObj.rawDataStruct.dtt_result;
            
            % check if it's a reference
            % this returns {} if it is not a reference
            result_name = dttxml_get_reference_result_name({chA_name,chB_name},dtt_result);
            chB_i = 1;
            
            if isempty(result_name)
                % the case that a reference is not requested
                
                % prepare A ch
                testName = 'CrossCorrelation';
                [chA_i,~] = dttxml_prepare_chan('A',testName,dtt_index,chA_name);
                
                if isempty(chA_i)
                    disp('Requested A channel not found!');
                    freq =[];
                    coh = [];
                    return
                end
                
                [chB_i,chB_len] = dttxml_prepare_chan('B',testName,dtt_index,chB_name);
                
                if isempty(chB_i)
                    disp('Requested B channel not found!');
                    freq =[];
                    tf_cmplx = [];
                    return
                end
                
                % DEBUG
                % chA_len = length(chA_list);
                
                % prepare B ch
                
                %                 res_list = dtt_index.CrossCorrelation.Name;
                %                 result_name = strrep(strrep(res_list{(chA_i-1)*chB_len+1},'[',''),']','');
                %                 data = dtt_result.(result_name);
                %
                %                 chB_list = strcmp(data.ChannelB,chB_name);
                %                 chB_i = find(chB_list,1);
                %
                %                 if isempty(chA_i)
                %                     disp('Requested A channel not found!');
                %                     freq = [];
                %                     coh  = [];
                %                     return
                %                 end
                
                res_list = unique(dtt_index.CrossCorrelation.Name);
                
                for res_i=1:length(res_list) % scan for all results
                    
                    result_name = strrep(strrep(res_list{res_i},'[',''),']','');
                    data = dtt_result.(result_name);
                    
                    % DEBUG
                    % disp([num2str(res_i) ': ' data.ChannelA ' : ' chA_name]);
                    
                    if strcmp(data.ChannelA,chA_name)
                        chB_list = strcmp(data.ChannelB,chB_name);
                        chB_i = find(chB_list,1);
                        
                        if isempty(chB_i)
                            error(['Requested B channel not found in ' result_name]);
                        else
                            % DEBUG
                            % disp(['Found ' chB_name ' in ' result_name]);
                            break
                        end
                    end
                end
                % DEBUG
                % chB_len = length(chB_list);
                
                
                %% Cross spectrum P_AB
                
                % extract data block
                corr_data = data.Data;
                
                % data total size
                corr_data_sz = size(corr_data);
                
                % convert to complex numbers
                corr_data_reshaped = reshape(corr_data, 2, corr_data_sz(2)/2);
                corr_data_reshaped_cmplx = corr_data_reshaped(1,:)+1i*corr_data_reshaped(2,:);
                
                % frequency bins
                f0 = str2double(data.f0);
                n  = str2double(data.N);
                df = str2double(data.df);
                
                freq = f0+(0:n-1)*df;
                
                % cut out the requested part
                cross_spe = corr_data_reshaped_cmplx((n*(chB_i-1)+1):(n*(chB_i)));
                
                %% Power spectrum sqrt(P_AA)
                
                [freq_tmp psdA] = powerSpectrum(dttObj, chA_name);
                
                %% Power spectrum sqrt(P_BB)
                
                [freq_tmp psdB] = powerSpectrum(dttObj, chB_name);
                
                %% Coherence: |P_BA|.^2/(P_AA P_BB)
                
                coh = abs(cross_spe).^2./psdA.^2./psdB.^2;
                
            else
                data = dtt_result.(result_name);
                
                % extract data block
                coh = data.Data;
                
                % frequency bins
                f0 = str2double(data.f0);
                n  = str2double(data.N);
                df = str2double(data.df);
                
                freq = f0+(0:n-1)*df;
            end
            
            % common part for a result data and a reference data
            
            freq = transpose(freq);
            coh = transpose(coh);
        end
        
        function [freq, psd] = powerSpectrum(dttObj,ch_name)
            
            dtt_index = dttObj.rawDataStruct.dtt_index;
            dtt_result = dttObj.rawDataStruct.dtt_result;
            
            % check if it's a reference
            % this returns {} if it is not a reference
            result_name = dttxml_get_reference_result_name({ch_name},dtt_result);
            
            if isempty(result_name)
                % the case that a reference is not requested
                
                % prepare ch
                res = strcmp(dtt_index.PowerSpectrum.Channel,ch_name);
                ch_i = find(res,1);
                
                if isempty(ch_i)
                    disp('Requested channel not found!');
                    freq =[];
                    psd = [];
                    return
                end
                
                name_list = dtt_index.PowerSpectrum.Name;
                result_name = strrep(strrep(name_list{ch_i},'[',''),']','');
            end
            
            data = dtt_result.(result_name);
            
            f0 = str2double(data.f0);
            n  = str2double(data.N);
            df = str2double(data.df);
            
            freq = f0+(0:n-1)*df;
            psd = data.Data; % /rtHz
            
        end
    end
    
    methods (Static)
        % static methods
        function objOut = readDttXml(filename, verbose)
            % open file
            fid = fopen(filename);
            
            % was opening file successful?
            if fid == -1
                error('file open not succesful')
            end
            
            tmp = textscan(fid, '%s','Delimiter','\n');
            tbuf = tmp{1};
            fclose(fid);
            tseek = 1;
            % if it was successful start our job
            
            % initialization of buffers
            data_buf=[];
            terminator = '</LIGO_LW>';
            
            
            % let's confirm if the file is dtt xml or not
            if verbose
                disp(['Reading the file.: ' filename]);
            end
            find_name = 'Diagnostics Test';
            %disp('Now, checking if the file is a dtt xml file.');
            tseek = dttxml_seek_block(tbuf, tseek, find_name, verbose);
            if tseek == 0
                error('The file does not seem to be a DTT xml file.');
            end
            
            % it seems it's dtt xml.
            
            %**********************
            % start reading the header
            %**********************
            
            if verbose
                disp('Trying to find the header');
            end
            find_name = 'Header';
            tseek = dttxml_seek_block(tbuf, tseek, find_name, verbose);
            if tseek == 0
                error('The header did not found.');
            end
            tseek_start = tseek-1;
            tseek = dttxml_read_until(tbuf, tseek, terminator, verbose);
            tseek_end = tseek-1;
            dtt_header = dttxml_parse_header({tbuf{tseek_start:tseek_end}});
            
            %**********************
            % start reading the synchronization block
            %**********************
            
            if verbose
                disp('Trying to find the synchronization block');
            end
            
            find_name = 'Synchronization';
            tseek = dttxml_seek_block(tbuf, tseek, find_name, verbose);
            
            if tseek == 0
                error('The sync block did not found.');
            end
            
            tseek_start = tseek-1;
            tseek = dttxml_read_until(tbuf, tseek, terminator, verbose);
            tseek_end = tseek-1;
            dtt_sync = dttxml_parse_sync({tbuf{tseek_start:tseek_end}});
            
            %**********************
            % start reading the test parameters
            %**********************
            
            if verbose
                disp('Trying to find the test parameter block');
            end
            
            find_name = 'TestParameter';
            tseek = dttxml_seek_block(tbuf, tseek, find_name, verbose);
            
            if tseek == 0
                error('The test parameter block did not found.');
            end
            
            tseek_start = tseek-1;
            tseek = dttxml_read_until(tbuf, tseek, terminator, verbose);
            tseek_end = tseek-1;
            dtt_test = dttxml_parse_test({tbuf{tseek_start:tseek_end}});
            
            %**********************
            % start reading the index parameters
            %**********************
            
            if verbose
                disp('Trying to find the index block');
            end
            
            find_name = 'Index';
            tseek = dttxml_seek_block(tbuf, tseek, find_name, verbose);
            
            if tseek == 0
                error('The index block did not found.');
            end
            
            tseek_start = tseek-1;
            tseek = dttxml_read_until(tbuf, tseek, terminator, verbose);
            tseek_end = tseek-1;
            dtt_index = dttxml_parse_index({tbuf{tseek_start:tseek_end}});
            
            %**********************
            % start reading the reference/result data
            %**********************
            if verbose
                disp('Trying to find the reference/result block');
            end
            
            find_name = 'Reference|Result';
            
            % our base64decode only works with java.
            error(javachk('jvm'))
            
            while 1
                
                tseek = dttxml_seek_block(tbuf, tseek, find_name, verbose);
                
                if tseek == 0
                    disp('');
                    if verbose
                        disp('Additional reference/result block not found. Ending');
                    end
                    break;
                end
                
                tseek_start = tseek-1;
                tseek = dttxml_read_until(tbuf, tseek, terminator, verbose);
                tseek_end = tseek-1;
                tmp = dttxml_parse_result({tbuf{tseek_start:tseek_end}}, verbose);
                dtt_result.(tmp.Name) = tmp;
                
            end
            
            if verbose
                dtt_result
            end
            
            dtt.dtt_header = dtt_header;
            dtt.dtt_sync = dtt_sync;
            dtt.dtt_test = dtt_test;
            dtt.dtt_index = dtt_index;
            dtt.dtt_result = dtt_result;
            
            objOut = DttData(dtt);
        end
        function typeCode = TransferFunctionSubtype(name)
            % T990013 page 57
            switch name
                case 'Coherence (f,Y)'
                    typeCode = 5;
                case 'B/A TransferFunction (f,Y)'
                    typeCode = 3;
                otherwise
                    typeCode = -1;
            end
        end
    end % methods (Static)
end