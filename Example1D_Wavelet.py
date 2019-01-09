#!/usr/bin/python -u

# the needed extern modules
import numpy as np

# own module
import sigmatransform as st

# setup
np.set_printoptions(precision=2,edgeitems=10,linewidth=120)
numsteps = 400.0;
winwidth = 4.0;

# the channels
Fs = 143000.0;
chan = np.linspace( np.log2(Fs*0.005) , np.log2(Fs/2.0*1.1) , numsteps );

# the diffeomorphism
def sig(x): 
    return np.log2( x * (x>0.0) );

# the adapted Gaussian window in warped domain
def win(x):
    return np.exp(-np.pi*( x / sig(Fs) * numsteps / winwidth )**2 );

# the signal
f = np.loadtxt("bat.asc");

# get an instance
Wavelet = st.SigmaTransform( 
    sig ,   # the diffeomorphism handle 
    win ,   # the window handle
    Fs  ,   # the sampling Frequency
    chan    # the channels in warped Fourier domain
);

# analyze the signal f (coeff is stored internally, so no need to capture "coeff" right now)...
Wavelet.analyze( f );
# ...and get coeffs
co = Wavelet.coeff;

# try to reconstruct "f" from its coefficients (without dual frame, so depends on the chosen channels)
# and store in "recVec"
recVec = Wavelet.synthesize().rec;

# plot the modulus of the ceofficients
Wavelet.plotCoeff();

# apply Wavelet-Multiplier...
Wavelet.analyze(f).applyMaskFunc(lambda x,y : (x>.5)*(y>10)+.5 ).synthesize();
#recMasked = Wavelet.rec;
Wavelet.plotCoeff();

# ...or, as a "one-liner":
recMasked = st.SigmaTransform(
    lambda x : np.log2( x * (x>0.0) ),
    lambda x : np.exp(-np.pi*( x / sig(Fs) * 400.0 / 4.0 )**2 ),
    143000, 
    np.linspace( np.log2(Fs*0.005) , np.log2(Fs/2.0*1.1) , 400 )
).multiplier(
    np.loadtxt("bat.asc"),
    lambda x,y : (x < .5)*(y>10) + .2
).plotCoeff();
