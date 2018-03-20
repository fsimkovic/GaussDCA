# GaussDCA (Cython)
Python implementation of GaussDCA using Cython. Adapted from [here](https://github.com/carlobaldassi/GaussDCA.jl).

For the original paper please refer to ["Fast and accurate multivariate Gaussian modeling of protein families: Predicting residue contacts and protein-interaction partners"](doi:10.1371/journal.pone.0092721) by Carlo Baldassi, Marco Zamparo, Christoph Feinauer, Andrea Procaccini, Riccardo Zecchina, Martin Weigt and Andrea Pagnani, (2014) PLoS ONE 9(3): e92721. 

This version implements what is called the "slow fallback" in the original Julia implementation. 

## Installation
Runs in Python 3.6
1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Compile the cython source code: `cd src; python setup.py build_ext -i; cd ..`

## Usage
```python gaussdca/gaussdca.py [-h] [-o OUTPUT] [-t THREADS] alignment_file alignment_format```

So far, the alignment format needs to be specified using one of [ConKit's data formats](http://conkit.org/en/latest/formats.html). The output will be printed or saved into a file if given. The number of threads for multiprocessing can be specified.

## Performance
The following chart shows the elapsed runtime in minutes for a large test alignment (test/large.a3m) using 8 cores.
![performance](https://github.com/MMichel/GaussDCA/blob/master/timing.png)

The first three bars show the effect of using different methods to do the matrix inversion:
+ [pinv](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.pinv.html): pseudoinverse from numpy.linalg (uses SVD)
+ [inv](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.inv.html): multiplicative inverse from numpy.linalg
+ inv(chol): computes the [Cholesky decomposition](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.cholesky.html) first and then inverts the matrix

The next bar "inv(chol) opt" uses the same inversion as above, but with some additional techincal optimizations.

The last bar "julia" shows the runtime of the [julia implementation](https://github.com/carlobaldassi/GaussDCA.jl) on 8 cores, with alignment compression.

Alignment compression has not been implemented yet.
