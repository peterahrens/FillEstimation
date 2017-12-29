# generate times matrix

import numpy as np
from util import *
from blockutil import *
import os
from sys import argv
from data_meta import *

# generate performance matrix
# python data_spmv_times.py [matrixdir] [outputdir] [architecture] [matrix_id]
matrix_id = argv[4]

matrix_name = matrices[int(matrix_id)]["name"]
print(matrix_name)

# generate references for matrix_name
ref = get_references([matrix_name])

outdir = os.path.join(ref_dir)
if not os.path.isdir(outdir):
    os.mkdir(outdir)

outfile = os.path.join(ref_dir, matrix_name)

# save
np.save(outfile, ref)
