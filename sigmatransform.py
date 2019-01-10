import numpy as np
import matplotlib.pyplot as plt

# the Gaussian window
def gauss(x): return np.exp(-np.pi*x.dot(x) );

class SigmaTransform:

    # constructor, simply stores the relevant information
    def __init__(self , sig=lambda x:x , win=gauss , Fs=1 , chan=[] , action=lambda x,y:x-y ):
        self.sig,self.win,self.Fs,self.action,self.chan=sig,win,Fs,action,chan.reshape(-1,1);

    # the forward transform, maps a signal "f" to its coefficients in "self.coeff"
    def analyze( self , f ):
        dom = self.sig( np.fft.ifftshift( np.linspace(-self.Fs/2.0 , self.Fs/2.0 , f.size ) ) )[None,...];
        self.len, self.windows = f.size, self.win( self.action( dom , self.chan ) );
        #plt.matshow( abs( self.windows ) ); plt.show();
        self.coeff = np.fft.ifftn( np.fft.fftn(f)[None,...] * self.windows.conjugate(), axes=range(1,len(self.windows.shape)));
        return self;

    # the adjoint transform
    def synthesize( self ):
        self.rec = np.fft.ifftn( (np.fft.fftn(self.coeff,axes=range(1,len(self.windows.shape))) * self.windows ).sum(0) );
        return self;

    # plots the coefficents, if the coefficients are representable as a matrix
    def plotCoeff( self ):
        plt.matshow( abs(self.coeff) ); plt.show();
        return self;

    # masks the coefficients 
    def applyMaskFunc(self,maskFunc):
        self.coeff *= maskFunc( np.linspace(0,1,self.len), self.chan );
        return self;

    # defines a multiplier. anaylze, mask, synthesize.
    def multiplier(self,f,maskFunc):
        self.analyze(f).applyMaskFunc(maskFunc).synthesize();
        return self;
