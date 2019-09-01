import control
import control.matlab
import scipy.io
import numpy as np

class SusModel(object):
    def __init__(self,matfile='hoge.mat'):
        mat_dict = scipy.io.loadmat(matfile)
        st = mat_dict['linss']
        # st = mat_dict['sys1']
        A,B,C,D,statename,outputname,inputname,operpoint,ts = st[0][0]
        # A = st[0][0][0]
        # B = st[0][0][1]
        # C = st[0][0][2]
        # D = st[0][0][3]
        # inputname = st[0][0][15]
        # outputname = st[0][0][18]
        self.A,self.B,self.C,self.D = A,B,C,D
        self.ss = control.matlab.ss(A, B, C, D)
        self.inputname = np.asarray([i[0][0] for i in inputname])
        self.outputname = np.asarray([i[0][0] for i in outputname])        

    def siso(self,inputname,outputname):
        prefix = 'controlmodel/'
        idx_from = np.where(self.inputname==prefix+inputname)[0][0]
        idx_to = np.where(self.outputname==prefix+outputname)[0][0]
        #print 'From :',idx_from,self.inputname[idx_from]
        #print 'To   :',idx_to,self.outputname[idx_to]
        out = self.ss.returnScipySignalLTI()
        ss = out[idx_to][idx_from]
        ss_siso = control.ss(ss.A,ss.B,ss.C,ss.D)
        #ss_siso = ss_siso.minreal()
        return ss_siso

    def ctrb(self):
        return control.ctrb(self.A,self.B)
        
class TypeA(SusModel):
    def __init__(self,matfile='/Users/miyo/Dropbox/Git/kagra-gif/armLengthCompensationSystem/vismodel/SuspensionControlModel/script/typeA/linmod.mat',actual=False):
        if not actual:
            super(TypeA,self).__init__(matfile)
            #super(TypeA,self).__init__()
        else:
            pass
        
if __name__ == "__main__":
    typea = SusModel('./SuspensionControlModel/script/typeA/linmod.mat')
    IPL2TML = typea.siso('controlmodel/noiseActIPL','controlmodel/dispTML')
    
