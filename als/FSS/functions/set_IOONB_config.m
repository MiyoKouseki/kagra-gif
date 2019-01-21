function [TTFSS_Gain,FB_SW_TTFSS,CMS_SW_IMC,FB_SW_MCL,CMS_SW_CARM,FB_SW_CARM,CavOpgain,LOOP_SW] = ...
    set_IOONB_config(varargin)
load('IOO_params.mat');

%% TTFSS
TTFSS_SW_List = {'CG','FG','Fast_Sign'};
TTFSS_default_list = [0,0,1];
TTFSS_Gain = containers.Map;
for ii = 1:length(TTFSS_SW_List)
    TTFSS_Gain(TTFSS_SW_List{ii}) = set_varargin([TTFSS_SW_List{ii}],TTFSS_default_list(ii),varargin);
    if TTFSS_Gain(TTFSS_SW_List{ii})>30
%        TTFSS_Gain(TTFSS_SW_List{ii})=30;
       warning('TTFSS gain is out of range')
    elseif TTFSS_Gain(TTFSS_SW_List{ii})<-10
%        TTFSS_Gain(TTFSS_SW_List{ii})=-10;
       warning('TTFSS gain is out of range')
    end
end


slow_gain = set_varargin('TEMPGAIN',0,varargin);
FB_SW_TTFSS = set_FB(slow_gain,[1]);

%% Common Mode Servo
% IMC
CMS_SW_List = {'IN1EN','IN2EN','FASTEN','IN1GAIN','IN2GAIN','FASTGAIN','IN1POL','IN2POL','FASTPOL','SLOWPOL',...
    'COMCOMP','COMBST','COMOPT','COMGEN','SLOWBST','SLOWCOMP','SLOWGEN','SLOWBY','SLOWOPT','FASTOPT'};
CMS_default_list = [0,0,0,0,0,0,1,1,1,1,...
    0,0,0,0,0,1,0,0,0,0];

% IMC
CMS_SW_IMC = containers.Map;
for ii = 1:length(CMS_SW_List)
    if strcmp(CMS_SW_List{ii},'IN1GAIN')||strcmp(CMS_SW_List{ii},'IN2GAIN')||strcmp(CMS_SW_List{ii},'FASTGAIN')
        if mnismember(varargin,[CMS_SW_List{ii} '_IMC'])
            if varargin{mnismember(varargin,[CMS_SW_List{ii} '_IMC'])+1}>31
                CMS_SW_IMC(CMS_SW_List{ii}) = varargin{mnismember(varargin,[CMS_SW_List{ii} '_IMC'])+1};
                warning('common mode servo gain is out of range')
            elseif varargin{mnismember(varargin,[CMS_SW_List{ii} '_IMC'])+1}<-32
                CMS_SW_IMC(CMS_SW_List{ii}) = varargin{mnismember(varargin,[CMS_SW_List{ii} '_IMC'])+1};
                warning('common mode servo gain is out of range')
            else
                CMS_SW_IMC(CMS_SW_List{ii}) = mn_CMSgain(varargin{mnismember(varargin,[CMS_SW_List{ii} '_IMC'])+1});
            end
        else
            CMS_SW_IMC(CMS_SW_List{ii}) = CMS_default_list(ii);
        end 
    else
        CMS_SW_IMC(CMS_SW_List{ii}) = set_varargin([CMS_SW_List{ii} '_IMC'],CMS_default_list(ii),varargin);
    end
end
CMS_SW_IMC('AOM_FAST') = set_varargin('AOM_FAST',0,varargin);
K1IMC_MCL_GAIN = set_varargin('K1IMC_MCL_GAIN',0,varargin);
K1IMC_MCL_FBSW = set_varargin('K1IMC_MCL_FBSW',[],varargin);
FB_SW_MCL = set_FB(K1IMC_MCL_GAIN, K1IMC_MCL_FBSW);

% CARM
CMS_SW_CARM = containers.Map;
for ii = 1:length(CMS_SW_List)
    if strcmp(CMS_SW_List{ii},'IN1GAIN')||strcmp(CMS_SW_List{ii},'IN2GAIN')||strcmp(CMS_SW_List{ii},'FASTGAIN')
        if mnismember(varargin,[CMS_SW_List{ii} '_CARM'])
            if varargin{mnismember(varargin,[CMS_SW_List{ii} '_CARM'])+1}>31
                CMS_SW_CARM(CMS_SW_List{ii}) = mn_CMSgain(31);
                warning('common mode servo gain is out of range')
            elseif varargin{mnismember(varargin,[CMS_SW_List{ii} '_CARM'])+1}<-32
                CMS_SW_CARM(CMS_SW_List{ii}) = mn_CMSgain(-32);
                warning('common mode servo gain is out of range')
            else
                CMS_SW_CARM(CMS_SW_List{ii}) = mn_CMSgain(varargin{mnismember(varargin,[CMS_SW_List{ii} '_CARM'])+1});
            end
        else
            CMS_SW_CARM(CMS_SW_List{ii}) = CMS_default_list(ii);
        end 
    else
        CMS_SW_CARM(CMS_SW_List{ii}) = set_varargin([CMS_SW_List{ii} '_CARM'],CMS_default_list(ii),varargin);
    end
end
K1LSC_CARM_SERVO_GAIN = set_varargin('K1:LSC-CARM_SERVO_GAIN',0,varargin);
K1LSC_CARM_SERVO_FBSW = set_varargin('K1:LSC-CARM_SERVO_FBSW',[],varargin);
FB_SW_CARM = set_FB(K1LSC_CARM_SERVO_GAIN, K1LSC_CARM_SERVO_FBSW);
%% Set optical gains
Cav_List = {'IMC','RefCav','CARM'};
CavOpgain = containers.Map;
opgain_default_list = [0 0 0];
for ii = 1:length(Cav_List)
    CavOpgain(Cav_List{ii}) = set_varargin(['Opgain_' Cav_List{ii}],opgain_default_list(ii),varargin);
end

%% set loop SW
LOOP_SW = set_varargin('LOOP_SW',ones([8 1]),varargin);

end

function output = set_varargin(name, default, argin)
    if mnismember(argin,name)
        output = argin{mnismember(argin,name)+1};
    else
        output = default;
    end 
end



