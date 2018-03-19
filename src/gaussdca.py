
from operator import itemgetter

import argparse
import conkit.core
import conkit.io
import numpy
import numpy as np
import os
import sys

#from _gaussdca_parallel import compute_gdca_scores
from _gaussdca_parallel_opt import compute_gdca_scores


def run_gdca(infile, informat, outfile='', num_threads=1):
    if not os.path.isfile(infile):
        sys.stderr.write("Alignment file not found.\n")
        sys.exit(1)

    ali = conkit.io.read(infile, informat).filter_gapped()
    aln = np.array(ali.encoded_matrix, dtype=np.int8, order="F").T

    gdca_dict = compute_gdca_scores(aln, num_threads=num_threads)
    gdca = gdca_dict["gdca"]
    gdca_corr = gdca_dict["gdca_corr"]

    cmap = to_contact_map(gdca_corr)
    if outfile:
        conkit.io.write(outfile, "casp", cmap)
    else:
        print(cmap.to_string())


def to_contact_map(scores):
    contact_map = conkit.core.ContactMap("1")
    for coord, value in np.ndenumerate(scores):
        if coord[0] < coord[1]:
            contact_map.add(conkit.core.Contact(coord[0] + 1, coord[1] + 1, value))
    contact_map.sort("raw_score", reverse=True, inplace=True)
    return contact_map


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Cython implementation of GaussDCA (doi:10.1371/journal.pone.0092721)")
    p.add_argument('alignment_file')
    p.add_argument('alignment_format')
    p.add_argument('-o', '--output', default='')
    p.add_argument('-t', '--threads', default=1, type=int)
    args = vars(p.parse_args(sys.argv[1:]))

    run_gdca(
        args['alignment_file'],
        args['alignment_format'],
        outfile=args['output'],
        num_threads=args['threads'],
    )
