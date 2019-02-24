#!/usr/bin/python -u

# the needed extern modules
import numpy as np

# own module
import sigmatransform as st

# setup
np.set_printoptions(precision=2,edgeitems=10,linewidth=120)

# the channels
Fs = 143000;
chan = np.linspace(-Fs/2.0,Fs/2.0,400);

# the Gaussian window
def win(x):
    return np.exp(-np.pi* ( x / Fs * 400 / 16.0 )**2 );

# the (trivial) diffeomorphism (for STFT)
def sig(x): return x;

# the signal
f = np.loadtxt("bat.asc");

# get an instance
STFT = st.SigmaTransform( 
    sig ,   # the diffeomorphism handle 
    win ,   # the window handle
    Fs  ,   # the sampling Frequency
    len(f), # the signal length
    chan    # the channels in warped Fourier domain
);

# analyze the signal f (coeff is stored internally, so no need to capture "coeff" right now)...
STFT.analyze( f );
# ...and get coeffs
co = STFT.coeff;

# try to reconstruct "f" from its coefficients (without dual frame, so depends on the chosen channels)
# and store in "recVec"
recVec = STFT.synthesize().rec;

# plot the modulus of the ceofficients
STFT.plotCoeff();

# apply multiplier...
STFT.analyze(f).applyMaskFunc(lambda x,y : (x>.5)*(y>0)+.5 ).synthesize();
recMasked = STFT.rec;
STFT.plotCoeff();

# ...or short:
recMasked = st.SigmaTransform(
    lambda x : x,
    lambda x : np.exp(-np.pi*(x/Fs*400.0/16.0)**2),
    143000, 
    400,
    np.linspace(-Fs/2.0,Fs/2.0,400)
).multiplier(
    np.loadtxt("bat.asc"),
    lambda x,y : (x < .5)*(y<0) + .2
).plotCoeff();
