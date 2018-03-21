
from operator import itemgetter

import argparse
import conkit.io
import numpy
import numpy as np
import os
import sys

from conkit.core import Contact, ContactMap
from conkit.plot import ContactMapMatrixFigure

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

    #  fig = ContactMapMatrixFigure(cmap)
    #  fig.ax.set_aspect(1.0)
    #  fig.savefig(infile + ".png", dpi=600)


def to_contact_map(scores):
    contact_map = ContactMap("1")
    for coord in zip(*np.triu_indices(scores.shape[-1])):
        contact_map.add(Contact(int(coord[0] + 1), int(coord[1] + 1), scores[coord]))
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
