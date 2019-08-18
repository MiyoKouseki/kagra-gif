
%% buildsusmodel (main)

function sus=buildsusmodel_old(sus)

% buildsusmodel constructs a state-space model of a suspension system using
% parameters stored in the input structure.

checkinput(sus);
sus = makeMGKmatrix(sus);
sus = makessmatrix(sus);

end




%% checkinput

function checkinput(sus)
% sanity check

if ~isstruct(sus)
    error('buildsusmodel:InputError',...
        'First argument should be a structure.')
end
if  ~isfield(sus,'g')
    error('buildsusmodel:InputError',...
        'Grounds must be set in the input strcture.')
end
if  ~isfield(sus,'b')
    error('buildsusmodel:InputError',...
        'Rigid bodies must be set in the input structure.')
end
if  ~isfield(sus,'w') && ~isfield(sus,'ip')
    error('buildsusmodel:InputError',...
        'Elastic components must be set in the input structure.')
end

end





%% makematrix

function sus=makeMGKmatrix(sus)
% make mass, damping, and stiffness matrices (matM, matG, matK)

g=9.81; % gravity constant

%% Set variables
gn=sus.g.n;  % ground name list
bn=sus.b.n;  % rigid body name list
bcn=[bn,gn]; % combined list
dn={'L','T','V','R','P','Y'}; % degrees of freedom

invar=cell(length(dn),length(gn));
stvar=cell(length(dn),length(bn));

for n=1:length(dn)
    for m=1:length(gn)
        invar{n,m}=strcat(dn{n},gn{m});
    end
end

for n=1:length(dn)
    for m=1:length(bn)
        stvar{n,m}=strcat(dn{n},bn{m});
    end
end

invar=reshape(invar,1,[]); % input variables
stvar=reshape(stvar,1,[]); % state variables



%% Create empty matrices [matM, matG, matK]
invl=length(invar);
stvl=length(stvar);
totvl=stvl+invl;

matM =zeros(totvl,totvl);
matK =zeros(totvl,totvl);
matG =zeros(totvl,totvl);



%% Set mass matrix [matM]
bm=sus.b.m;  % mass
bI=sus.b.I;  % moment of inertia

for n=1:length(bn)
    
    matM((n-1)*6+1:(n-1)*6+6,(n-1)*6+1:(n-1)*6+6)=...
        [...
        eye(3)*bm{n}, zeros(3);...
        zeros(3)    , bI{n}   ;...
        ];
    
end





%% Stiffness matrix [matK] and mass matrix [matM] about wires

wn =sus.w.n;  % number of wires
wop=sus.w.op; % option
wub=sus.w.ub; % upper body
wlb=sus.w.lb; % lower body
wg =sus.w.g;  % geometric parameters [m]
wl =sus.w.l;  % wire length [m]
wd =sus.w.d;  % wire diameter [m]
wt =sus.w.t;  % total load [kg]
wy =sus.w.y;  % Young's modulus [N/m2]
ws =sus.w.s;  % shear modulus [N/m2]
wQ =sus.w.Q;  % Quality factor
wai=sus.w.ai; % Arbitrary inputs

nwl=length(sus.w.ub); % element number of wire list

for n=1:nwl
    % PARAMETER SET
    % option
    wopn = wop{n};
    % arbitrary input
    wain = wai{n};
    wainnl=cell(length(wain));
    for nwai=1:length(wain)
        wainnl=wain{nwai}{1};  % arbitrary input titles
    end
    % number of wires
    wnn=wn{n};
    % bodies numbering
    nwubn = find(strcmp(bcn,wub{n}));  % upper body #
    nwlbn = find(strcmp(bcn,wlb{n}));  % lower body #
    % diameter
    wdn=wd{n}(1);                           % waist diameter [m]
    if ~isempty(wopn(strcmp('neck',wopn))) % if 'neck' option exists
        wdnn=wd{n}(2);                     % set neck diameter
    else                                   % if 'neck' option doesn't exist
        wdnn=wd{n}(1);                     % neck diameter = waist diameter
    end
    % length
    wln=wl{n}(1);                          % total length [m]
    if ~isempty(wopn(strcmp('neck',wopn))) % if 'neck' option exists
        wlnn=wl{n}(2);                     % set neck length
    else                                   % if 'neck' option doesn't exist
        wlnn=0;                            % set neck length zero
    end
    % wire inclination
    wdwn=0;                          % horizontal distance (w1)
    whn=sqrt(wln^2-wdwn^2);          % vertical distance (h0)
    % load
    wtn=wt{n}*g;                     % total load on wires[N]
    wten=wtn*(wln/whn)/wnn;          % tension on each wire [N]
    % material property
    wyn=wy{n};                       % Young's modulus [N/m2]
    wsn=ws{n};                       % shear modulus [N/m2]
    wQn=wQ{n};                       % quality factor
    % wire geometry
    warean=pi*wdn^2/4;                % area [m2]
    wareann=pi*wdnn^2/4;              % neck area [m2]
    if (wten/wareann)>1e9             % alart if stress exceeds 1 [GPa]
        warning('buildsusmodel:wire',...
            ['Wire stress (',...
            num2str(wten/warean/1e9),' GPa) exceeds 1 GPa',...
            ' in the wire set #',num2str(n)])
    end
    wsmoann=pi*wdnn^4/64;            % second area moi at neck [m4]
    wpsmoan=pi*wdn^4/32;             % polar second area moi [m4]
    wpsmoann=pi*wdnn^4/32;           % polar second area moi at neck [m4]
    % bending point compensation
    if ~isempty(wopn(strcmp('nobend',wopn))) % if option 'nobend' exists
        weffbn=0;                            % no compensation
    else                                     % if option 'nobend' not exists
        weffbn=sqrt(wyn*wsmoann/wten);       % effective bending length [m]
    end
    if (weffbn/wln)>0.3                      % too thick wires
        error('buildsusmodel:wire',...
            ['The wire is too thick with given wire tension. ',...
            'Effective bending length exceeds 30% of the',...
            'wire length in the wire set #',num2str(n)],'. ',...
            'Stiffness matrix cannot be calculated.')
    end
    % wlneff=wln-2*weffbn;                % wire effective length [m]
    wh1n=wg{n}(1);                      % wire bending point upper [m]
    wh2n=wg{n}(2);                      % wire bending point lower [m]
    % wh1neff=wg{n}(1)-weffbn;            % wire effective bending point upper [m]
    % wh2neff=wg{n}(2)+weffbn;            % wire effective bending point lower [m]
    
    % bounce mode stiffness
    if ~isempty(wopn(strcmp('spring',wopn)))   % if option 'spring' exists
        wspargn=wain{strcmp('spring',wainnl)}; % find spring argument
        wfspn=wspargn{2};                      % frequency [Hz]
        wQsn =wspargn{4};                      % Q factor about tensile mode
        wBspn=wspargn{3};                      % Saturation level 
        wksns=wten/g*(2*pi*wfspn(1))^2;        % spring stiffnerss [N/m]
        wksnw=wyn/((wln-2*wlnn)/warean+2*wlnn/wareann); % wire stiffness [N/m]
        wksn=wksns*wksnw/(wksns+wksnw);        % tensile stiffness [N/m]
    else                                       % if option 'spring' not exists
        wQsn=wQn;                              % Q factor about tensile mode
        wBspn=0;                               % no saturation
        wksn=wyn/((wln-2*wlnn)/warean+2*wlnn/wareann); % tensile stiffness [N/m]
    end
    wktn=wsn/((wln-2*wlnn)/wpsmoan+2*wlnn/wpsmoann);
                                    % torsional stiffness [Nm/rad]
                                    
    % STIFFNESS MATRIX
    switch wnn
        case 1
            matKwn=makematKwn1(wten,wln,wh1n,wh2n,weffbn,wQn,wQsn,wksn,wktn);
        case 2
            ww1n=wg{n}(3);  % wire separation in T direction
            matKwn=makematKwn2(wten,wln,wh1n,wh2n,weffbn,ww1n,wQn,wQsn,wksn,wktn);
        case 3
            wr1n=wg{n}(3);  % wire separation from center
            matKwn=makematKwn3(wten,wln,wh1n,wh2n,weffbn,wr1n,wQn,wQsn,wksn,wktn);
        case 4
            ww1n=wg{n}(3);  % wire separation in T direction
            wd1n=wg{n}(4);  % wire separation in L direction
            matKwn=makematKwn4(wten,wln,wh1n,wh2n,weffbn,ww1n,wd1n,wQn,wQsn,wksn,wktn);
    end
    
    nwubx=6*(nwubn-1);
    nwlbx=6*(nwlbn-1);
    matK([nwubx+1:nwubx+6,nwlbx+1:nwlbx+6],...
         [nwubx+1:nwubx+6,nwlbx+1:nwlbx+6])=...
         matK([nwubx+1:nwubx+6,nwlbx+1:nwlbx+6],...
         [nwubx+1:nwubx+6,nwlbx+1:nwlbx+6])+matKwn;
    
    matM([nwubx+3,nwlbx+3],[nwubx+3,nwlbx+3])=...
       matM([nwubx+3,nwlbx+3],[nwubx+3,nwlbx+3])+...
       [0 wtn/g*wBspn;
       wtn/g*wBspn 0];
    
end


%% Dampint matrix [matG] by dampers

if isfield(sus,'d')
db1=sus.d.b1; % body1
db2=sus.d.b2; % body2
dp1=sus.d.p1; % damping point at body1
dp2=sus.d.p2; % damping point at body2
dmat=sus.d.m; % damping coefficient matrix
ndmp=length(db1); % number of damper list

for n=1:ndmp
 ndb1 =find(strcmp(bcn,db1{n})); % body1 #
 ndb2 =find(strcmp(bcn,db2{n})); % body2 #
 ndb1x=6*(ndb1-1);
 ndb2x=6*(ndb2-1);
 dmatn=dmat{n};  % damping matrix
 dp1n=dp1{n};    % damping position at body1
 dp2n=dp2{n};    % damping position at body2
 pmat1n=[...
     1, 0, 0,        0, +dp1n(3), -dp1n(2);...
     0, 1, 0, -dp1n(3),        0, +dp1n(1);...
     0, 0, 1, +dp1n(2), -dp1n(1),        0;...
     0, 0, 0, 1, 0, 0;...
     0, 0, 0, 0, 1, 0;...
     0, 0, 0, 0, 0, 1 ...
     ];
 pmat2n=[...
     1, 0, 0,        0, +dp2n(3), -dp2n(2);...
     0, 1, 0, -dp2n(3),        0, +dp2n(1);...
     0, 0, 1, +dp2n(2), -dp1n(1),        0;...
     0, 0, 0, 1, 0, 0;...
     0, 0, 0, 0, 1, 0;...
     0, 0, 0, 0, 0, 1 ...
     ];
 
 matG(ndb1x+1:ndb1x+6,ndb1x+1:ndb1x+6)=...
     matG(ndb1x+1:ndb1x+6,ndb1x+1:ndb1x+6)+...
     pmat1n'*dmatn*pmat1n;
 matG(ndb1x+1:ndb1x+6,ndb2x+1:ndb2x+6)=...
     matG(ndb1x+1:ndb1x+6,ndb2x+1:ndb2x+6)+...
     pmat1n'*dmatn*pmat2n;
 matG(ndb2x+1:ndb2x+6,ndb1x+1:ndb1x+6)=...
     matG(ndb2x+1:ndb2x+6,ndb1x+1:ndb1x+6)+...
     pmat2n'*dmatn*pmat1n;
 matG(ndb2x+1:ndb2x+6,ndb2x+1:ndb2x+6)=...
     matG(ndb2x+1:ndb2x+6,ndb2x+1:ndb2x+6)+...
     pmat2n'*dmatn*pmat2n;
 
end

end

%% matM and matK by inverted pendulum

if isfield(sus,'i')

% IP
ipbb=sus.i.bb;
ipsb=sus.i.sb;
ipm=sus.i.m;
ipr=sus.i.r;
ipl=sus.i.l;
ipf=sus.i.f;
ipQ=sus.i.Q;
ipcp=sus.i.cp;
ipkt=sus.i.kt;
nip=length(ipbb);

for n=1:nip
    
    nipbb =find(strcmp(bcn,ipbb{n})); % base body #
    nipsb =find(strcmp(bcn,ipsb{n})); % upper body #
    nipbbx=6*(nipbb-1);
    nipsbx=6*(nipsb-1);
    
    ipQn=ipQ{n};   % Q factor of translation mode
    ipasn=ipm{n}*g/ipl{n}; % anti-spring coefficients
    
    ipkLn=ipm{n}*(2*pi*ipf{n})^2;  % translatoin stiffness 
    ipkYn=ipm{n}*(2*pi*ipf{n})^2*ipr{n}^2+ipkt{n}; % torsion stiffness
    ipkPn=(ipasn+ipkLn)*ipl{n};    % coupling from pitch
    
    ipkLni=ipkPn/ipl{n}/ipQn;     % translation
    ipkYni=(ipkPn/ipl{n}*ipr{n}^2+ipkt{n})/ipQn; % rotation
    ipkPni=ipkPn/ipQn;            % pitch
    
    matK(nipsbx+1,[nipbbx+1,nipbbx+5,nipsbx+1])=...
        matK(nipsbx+1,[nipbbx+1,nipbbx+5,nipsbx+1])+...
        [-(ipkLn+1i*ipkLni),-(ipkPn+1i*ipkPni),+(ipkLn+1i*ipkLni)];
    matK(nipsbx+2,[nipbbx+2,nipbbx+4,nipsbx+2])=...
        matK(nipsbx+2,[nipbbx+2,nipbbx+4,nipsbx+2])+...
        [-(ipkLn+1i*ipkLni),+(ipkPn+1i*ipkPni),+(ipkLn+1i*ipkLni)];
    matK(nipsbx+6,[nipbbx+6,nipsbx+6])=...
        matK(nipsbx+6,[nipbbx+6,nipsbx+6])+...
        [-(ipkYn+1i*ipkYni) +(ipkYn+1i*ipkYni)];
    
    mipcpn=ipm{n}*ipcp{n};
    matM([nipbbx+1,nipsbx+1],[nipbbx+1,nipsbx+1])=...
        matM([nipbbx+1,nipsbx+1],[nipbbx+1,nipsbx+1])+...
        mipcpn*[0 1;1 0];
    matM([nipbbx+2,nipsbx+2],[nipbbx+2,nipsbx+2])=...
        matM([nipbbx+2,nipsbx+2],[nipbbx+2,nipsbx+2])+...
        mipcpn*[0 1;1 0];
    
end


%% REMOVE UNNECESSARY DOF
iprmflg=zeros(2,nip*3);
for n=1:nip
    iprmflg(1,(n-1)*3+1)=find(strcmp(invar,['V',ipbb{n}]))+length(stvar);
    iprmflg(2,(n-1)*3+1)=find(strcmp(stvar,['V',ipsb{n}]));
    iprmflg(1,(n-1)*3+2)=find(strcmp(invar,['R',ipbb{n}]))+length(stvar);
    iprmflg(2,(n-1)*3+2)=find(strcmp(stvar,['R',ipsb{n}]));
    iprmflg(1,(n-1)*3+3)=find(strcmp(invar,['P',ipbb{n}]))+length(stvar);
    iprmflg(2,(n-1)*3+3)=find(strcmp(stvar,['P',ipsb{n}]));
end

for m=1:nip*3
   matK(:,iprmflg(1,m))=matK(:,iprmflg(1,m))+matK(:,iprmflg(2,m));
   matG(:,iprmflg(1,m))=matG(:,iprmflg(1,m))+matG(:,iprmflg(2,m));
end

logrmflg1=true(1,length(stvar));
for m=1:nip*3
    logrmflg1(iprmflg(2,m))=false;
end
logrmflg2=true(1,length(invar));
logrmflg=[logrmflg1,logrmflg2];


matM=matM(logrmflg,logrmflg);
matK=matK(logrmflg,logrmflg);
matG=matG(logrmflg,logrmflg);
stvar=stvar(logrmflg1);

end

sus.m.inv=invar;
sus.m.stv=stvar;


sus.m.matM=matM;
sus.m.matG=matG;
sus.m.matK=matK;

end


%% makessmatrix

function sus=makessmatrix(sus)

invl=sus.m.inv;
stvl=sus.m.stv;
ni=length(invl);
ns=length(stvl);

matM=sus.m.matM(1:ns,1:ns);
matG=sus.m.matG(1:ns,1:ns);
matK=sus.m.matK(1:ns,1:ns);
matMg=sus.m.matM(1:ns,ns+1:ns+ni);
matGg=sus.m.matG(1:ns,ns+1:ns+ni);
matKg=sus.m.matK(1:ns,ns+1:ns+ni);

%% structural damping -> viscous damping

[eigV,eigD] = eig(real(matK),matM); % eigen mode
eigW  = real(sqrt(eigD));           % eigen freq
eigW  = diag(diag(eigW)+0.01);      % avoid INF
matGs = (eigV)'/(eigW)*eigV*imag(matK); % damping
matG  = matG + diag(diag(matGs));
matK  = real(matK);
matKg = real(matKg);

%% save1
sus.m2.matM =matM;
sus.m2.matK =matK;
sus.m2.matG =matG;
sus.m2.matMg=matMg;
sus.m2.matKg=matKg;
sus.m2.matGg=matGg;

%% input/state variables
stvv=stvl;
stvf=stvl;
for n=1:ns
    stvv{n}=['vel',stvl{n}];
    stvf{n}=['act',stvl{n}];
end
invar=[invl,stvf];
stvar=[stvv,stvl];

%% make ABCD matrices
matA=[-matM\matG,-matM\real(matK);
    eye(ns),zeros(ns,ns)];
matB=[-matM\real(matKg),matM\eye(ns);
    zeros(ns,ni),zeros(ns,ns)];
matC=eye(2*ns);
matD=zeros(2*ns,ns+ni);
smdlss=ss(matA,matB,matC,matD,'statename',stvar,'inputname',invar,'outputname',stvar);

sus.ss=smdlss;

end

