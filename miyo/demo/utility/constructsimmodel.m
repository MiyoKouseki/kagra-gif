
% ---------------------------------------------------------------- %
% The function 'constructsimmodel' constructs a simulink model from
% given lists of input & output variable names for a suspension
% state-space model. Following arguments are required:
%   modelname    : model name
%   smdl         : state-space model
%   namemdl      : name of state-space model to be called in simulink
%   varinputsim  : input variable list
%   varoutputsim : output variable list
% ---------------------------------------------------------------- %

function constructsimmodel(modelname,smdl,namemdl,...
    varinputsim,varoutputsim)

%% Check
if ~ischar(modelname)||~ischar(namemdl)
    error('constructsimmodel:InputError',...
       'Argument [modelname]/[namemdl] must be a string.')
end

%% Input / Output List 

varinput=smdl.InputName;
varoutput=smdl.OutputName;
namessA=[namemdl,'.A'];
namessB=[namemdl,'.B'];
namessC=[namemdl,'.C'];
namessD=[namemdl,'.D'];
namessmod='''SUS_SS_MODEL''';

Nsasin=length(varinput);
Nsasout=length(varoutput);

if iscellstr(varinputsim)&&iscellstr(varoutputsim)
    Nsimin1=length(varinputsim);
    Nsimout1=length(varoutputsim);
else
   error('constructsimmodel:InputError',...
       'Wrong data type: varinputsim/varoutputsim') 
end

activatein=zeros(Nsasin);
activateout=zeros(Nsasout);

for n=1:Nsimin1
    for m=1:Nsasin
    activatein(m)=min([activatein(m)+strcmp(varinputsim(n),varinput(m)),1]);
    end 
end

for n=1:Nsimout1
    for m=1:Nsasout
    activateout(m)=min([activateout(m)+strcmp(varoutputsim(n),varoutput(m)),1]);
    end 
end

indexlistin=find(activatein);
indexlistout=find(activateout);

Nsimin=length(indexlistin);
Nsimout=length(indexlistout);

varinputsim2=cell(Nsimin);
varoutputsim2=cell(Nsimout);

for n=1:Nsimin
    varinputsim2{n}=varinput{indexlistin(n)};
end

for n=1:Nsimout
    varoutputsim2{n}=varoutput{indexlistout(n)};
end

%% Model Construction

% Model open
open_system(new_system(modelname));
simulink('open');

% Make subsystem
modelsasname=[modelname,'/Suspension'];
add_block('built-in/SubSystem', modelsasname);
sizesasblk=max(100,max([Nsasin,Nsasout])*5);
set_param(modelsasname,'Position',makepos(250,50+sizesasblk/2,150,sizesasblk));

% Make ss block in subsystem
blocknamess='SAS State-Space';
blockname_ss=[modelsasname,'/',blocknamess];
add_block('Simulink/Continuous/State-Space',blockname_ss);
set_param(blockname_ss,'A',namessA,'B',namessB,'C',namessC,'D',namessD,...
    'ContinuousStateAttributes',namessmod);
posyss=max([100+Nsasin*10,100+Nsasout*10]);
set_param(blockname_ss,'Position',makepos(300,posyss,50,50));

% make mux in subssytem
blocknamemux='mux';
blockname_mux=[modelsasname,'/',blocknamemux];
add_block('Simulink/Signal Routing/Mux',blockname_mux);
set_param(blockname_mux,'Inputs',num2str(Nsasin));
set_param(blockname_mux,'Position',makepos(200,posyss,5,Nsasin*20));

% make demux in subsystem
blocknamedemux='demux';
blockname_demux=[modelsasname,'/',blocknamedemux];
add_block('Simulink/Signal Routing/Demux',blockname_demux);
set_param(blockname_demux,'Outputs',num2str(Nsasout));
set_param(blockname_demux,'Position',makepos(400,posyss,5,Nsasout*20));

% add line between blocks
add_line(modelsasname,[blocknamemux,'/1'],[blocknamess,'/1']);
add_line(modelsasname,[blocknamess,'/1'],[blocknamedemux,'/1']);


%% Input / Output Construction

for n=1:Nsasin
    blockname_tmp=[modelsasname,'/',varinput{n}];
    if activatein(n)
        add_block('Simulink/Sources/In1',blockname_tmp);
        set_param(blockname_tmp,'Position',makepos(100,50+n*40,25,13));
    else
        add_block('Simulink/Sources/Constant',blockname_tmp,'Value','0');
        set_param(blockname_tmp,'Position',makepos(100,50+n*40,25,25));
    end
    add_line(modelsasname,[varinput{n},'/1'],[blocknamemux,'/',num2str(n)]);
end

for n=1:Nsasout
    blockname_tmp=[modelsasname,'/',varoutput{n}];
    if activateout(n)
        add_block('Simulink/Sinks/Out1',blockname_tmp);
        set_param(blockname_tmp,'Position',makepos(500,50+n*40,25,13));
    else
        add_block('Simulink/Sinks/Terminator',blockname_tmp);
        set_param(blockname_tmp,'Position',makepos(500,50+n*40,25,25));
    end
    add_line(modelsasname,[blocknamedemux,'/',num2str(n)],[varoutput{n},'/1']);
end

%% Input / Output Construction 2

for n=1:Nsimin
    blockname_tmp=[modelname,'/',varinputsim2{n}];
    add_block('Simulink/Sources/In1',blockname_tmp);
    set_param(blockname_tmp,'Position',makepos(100,50+n*40,25,13));
    add_line(modelname,[varinputsim2{n},'/1'],['Suspension','/',num2str(n)]);
end

for n=1:Nsimout
    blockname_tmp=[modelname,'/',varoutputsim2{n}];
    add_block('Simulink/Sinks/Out1',blockname_tmp);
    set_param(blockname_tmp,'Position',makepos(400,50+n*40,25,13));
    add_line(modelname,['Suspension','/',num2str(n)],[varoutputsim2{n},'/1']);
end

%% Save System
simulink('close');
% save_system(modelname,['simmodel/',modelname]);
save_system(modelname);
close_system(modelname);

