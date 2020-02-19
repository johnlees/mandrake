# vim: set fileencoding=<utf-8> :
# Copyright 2020 John Lees and Gerry Tonkin-Hill

'''Methods for setting up and running SCE, saving
and loading results'''

import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import squareform
from scipy.sparse import coo_matrix, csr_matrix
from .utils import sparse_joint_probabilities

# C++ extensions
from SCE import wtsne

# from .utils import distVec, distVecCutoff

# Run exits if fewer samples than this
MIN_SAMPLES = 100
DEFAULT_THRESHOLD = 1.0

def generateIJP(names, output_prefix, P, preprocessing, perplexity):
    if (len(names) < MIN_SAMPLES):
        sys.stderr.write("Less than minimum number of samples used (" + str(MIN_SAMPLES) + ")\n")
        sys.stderr.write("Distances calculated, but not running SCE\n")
        sys.exit(1)
        
    pd.Series(names).to_csv(output_prefix + 'names.txt', sep='\n', header=False, index=False)

    # convert to similarity
    P = distancePreprocess(P, preprocessing, perplexity)

    _saveDists(output_prefix, P.row, P.col, P.data)
    return(P.row, P.col, P.data)

def distancePreprocess(P, preprocessing, perplexity):
    if preprocessing:
        # entropy preprocessing 
        P = distancePreprocess(P, preprocessing, perplexity)
    else:
        P.data = 1 - P.data/np.max(P.data)
        P = P + D.T
        # Normalize
        sum_P = np.maximum(P.sum(), MACHINE_EPSILON)
        P /= sum_P
    return P

def loadIJP(npzfilename):
    npzfile = np.load(npzfilename)
    I = npzfile['I']
    J = npzfile['J']
    P = npzfile['P']
    return I, J, P

def runSCE(I, J, P, weight_file, names, SCE_opts):
    weights = np.ones((len(names)))
    if (weight_file):
        weights_in = pd.read_csv(weights, sep="\t", header=None, index_col=0)
        if (weights_in.index.symmetric_difference(names)):
            sys.stderr.write("Names in weights do not match sequences - using equal weights\n")
        else:
            intersecting_samples = weights_in.index.intersection(names)
            weights = weights_in.loc[intersecting_samples]
    
    embedding = np.array(wtsne(I, J, P, weights, 
                               SCE_opts['maxIter'], 
                               SCE_opts['cpus'], 
                               SCE_opts['nRepuSamp'], 
                               SCE_opts['eta0'], 
                               SCE_opts['bInit']))
    embedding = embedding.reshape(-1, 2)
    return(embedding)

def saveEmbedding(embedding, output_prefix):
    np.savetxt(output_prefix + ".embedding.txt", embedding)

# Internal functions

def _saveDists(output_prefix, I, J, P):
    np.savez(output_prefix, I=I, J=J, P=P)