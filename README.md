
# SigmaTransform-Python
Implements the Sigma Transform in Python

## Contents
- [General Information](#general-information)
- [Usage and Examples](#usage-and-examples)

# General information
This repository shows an exemplary implementation of the "SigmaTransform", as defined in the thesis _"Quantum Frames and Uncertainty Principles arising from Symplectomorphisms"_, written in Python.

Note that this library is not intended to show maximal performance, but show the usability of the universal interface of the "Sigma Transform" to perform well-known signal processing transforms / algorithms like the Short-Time Fourier Transform and Wavelet Transform.

Currently, only the one-dimensional SigmaTransform is implemented and utilizes NumPy and Matplotlib.

# Usage and Examples
Clone this repository, or copy the file "sigmatransform.py" to a local folder.
## Usage
Perform a STFT on a signal "f" and save coefficients as numpy array
```python
import sigmatransform as st
...
# define diffeomorphism
sig = lambda x : x;
# get an instance
STFT = st.SigmaTransform( 
    sig ,   # the diffeomorphism handle 
    win ,   # the window handle
    Fs  ,   # the sampling Frequency
    chan    # the channels in warped Fourier domain
);
# analyze the signal "f", given as numpy array ...
STFT.analyze( f );
# ...and get coeffs, as numpy array
coeff = STFT.coeff;
```

Perform a Wavelet transform on a signal "f" and plot coefficients
```python
import sigmatransform as st
...
# define diffeomorphism
sig = lambda x : np.log2(x*(x>0));
# get an instance
Wavelet = st.SigmaTransform( 
    sig ,   # the diffeomorphism handle 
    win ,   # the window handle
    Fs  ,   # the sampling Frequency
    chan    # the channels in warped Fourier domain
);
# analyze the signal "f", given as numpy array ...
Wavelet.analyze( f );
# ... and plot coeffs
Wavelet.plotCoeff();
```

## Examples
The python scripts
```
    Example1D_STFT.py
    Example1D_Wavelet.py
```
provide more elaborated usage examples.
