# vim: set fileencoding=<utf-8> :
# Copyright 2020 John Lees

'''Sketchlib functions for database construction'''

import os
import sys
import subprocess
import numpy as np

import h5py

def getSketchSize(dbPrefix):
    """Determine sketch size, and ensures consistent in whole database

    ``sys.exit(1)`` is called if DBs have different sketch sizes

    Args:
        dbprefix (str)
            Prefix for mash databases

    Returns:
        sketchSize (int)
            sketch size (64x C++ definition)
    """
    ref_db = h5py.File(dbPrefix, 'r')
    prev_sketch = 0
    for sample_name in list(ref_db['sketches'].keys()):
        sketch_size = ref_db['sketches/' + sample_name].attrs['sketchsize64']
        if prev_sketch == 0:
            prev_sketch = sketch_size
        elif sketch_size != prev_sketch:
            sys.stderr.write("Problem with database; sketch sizes for sample " +
                             sample_name + " is " + str(prev_sketch) +
                             ", but smaller kmers have sketch sizes of " + str(sketch_size) + "\n")
            sys.exit(1)

    return int(sketch_size)

def getKmersFromReferenceDatabase(dbPrefix):
    """Get kmers lengths from existing database

    Args:
        dbPrefix (str)
            Prefix for sketch DB files
    Returns:
        kmers (list)
            List of k-mer lengths used in database
    """
    ref_db = h5py.File(dbPrefix, 'r')
    db_kmer_sizes = []
    for sample_name in list(ref_db['sketches'].keys()):
        kmer_size = ref_db['sketches/' + sample_name].attrs['kmers']
        if len(db_kmer_sizes) == 0:
            db_kmer_sizes = kmer_size
        elif np.any(kmer_size != db_kmer_sizes):
            sys.stderr.write("Problem with database; kmer lengths inconsistent: " +
                             str(kmer_size) + " vs " + str(db_kmer_sizes) + "\n")
            sys.exit(1)

    db_kmer_sizes.sort()
    return list(db_kmer_sizes)

def readDBParams(dbPrefix):
    """Get kmers lengths and sketch sizes from existing database

    Calls :func:`~getKmersFromReferenceDatabase` and :func:`~getSketchSize`
    Uses passed values if db missing

    Args:
        dbPrefix (str)
            Prefix for sketch DB files

    Returns:
        kmers (list)
            List of k-mer lengths used in database
        sketch_sizes (list)
            List of sketch sizes used in database
    """

    db_kmers = getKmersFromReferenceDatabase(dbPrefix)
    if len(db_kmers) == 0:
        sys.stderr.write("Couldn't find  sketches in " + dbPrefix + "\n")
        sys.exit(1)
    else:
        kmers = db_kmers
        sketch_sizes = getSketchSize(dbPrefix)

    return kmers, sketch_sizes


def getSeqsInDb(dbname):
    """Return an array with the sequences in the passed database

    Args:
        dbname (str)
            Sketches database filename

    Returns:
        seqs (list)
            List of sequence names in sketch DB
    """
    seqs = []
    ref = h5py.File(dbname, 'r')
    for sample_name in list(ref['sketches'].keys()):
        seqs.append(sample_name)

    return seqs


