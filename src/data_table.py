import numpy as np
from util import *
from blockutil import *
import os
from sys import argv
from data_meta import *

n = 10
phil_delta = 0.01

# python data_table.py [matrixdir] [outputdir] [architecture] [matrix_id]
matrix_id = argv[4]

matrix_name = matrices[int(matrix_id)]["name"]

# load machine performance profile
perf_matrix = np.load(os.path.join(profile_dir, "profile.npy"))

oski_time = phil_time = oski_err = phil_err = oski_err_std =phil_err_std = oski_spmv = phil_spmv = oski_spmv_std = phil_spmv_std = 0

# make sure all the input files exist
reffile = os.path.join(ref_dir, matrix_name + '.npy')
spmvfile = os.path.join(spmv_times_dir, matrix_name + '.npy')
assert os.path.isfile(reffile)
assert os.path.isfile(spmvfile)

# load in reference and spmv times
reference = np.load(reffile)
matrix_times = np.load(spmvfile)

for method in methods:
    point = method["point"]
    
    # get time to do spmv with (0,0)
    base_time = matrix_times[0][0]

    # results = get errors from default fill estimate
    results = fill_estimates(method["name"], [matrix_name], B = B, results = True, trials = trials, **point)
    get_errors(results, [reference])
 
    spmv_times = []
    
    # get spmv time
    for estimate in results[0]['results']:
      # get block size
      blocksize = get_blocksize(estimate, perf_matrix)
    
      # look up time that multiplying by with blocksize would take
      spmv_times.append(matrix_times[blocksize[0]][blocksize[1]] / base_time )
    
    if method["name"] == 'oski':
        # update all oski lists
        # normalized time to estimate
        oski_time = results[0]["time_mean"] / base_time
        
        # error and std
        oski_err = np.mean(results[0]["errors"])
        oski_err_std = np.std(results[0]["errors"])

        # spmv and std
        oski_spmv = np.mean(spmv_times)
        oski_spmv_std = np.std(spmv_times)
    else:
        # update all phil lists
        # normalized time to estimate
        phil_time = results[0]["time_mean"] / base_time
        # error and std
        phil_err = np.mean(results[0]["errors"])
        phil_err_std = np.std(results[0]["errors"])

        # spmv and std
        phil_spmv = np.mean(spmv_times)
        phil_spmv_std = np.std(spmv_times)
       
# outputfiles
# in the format 
# for spmv times and 
# matrix_name phil_val phil_std oski_val oski_std

# for runtime, we just have val
# matrix_name phil_val 
# files (normalized time to estimate, error, normalized spmv time) in the form 
# matrix_id phil oski

time_path = os.path.join(table_dir, out_times_prefix + '_' + matrix_name)
err_path = os.path.join(table_dir, out_err_prefix + '_' + matrix_name)
spmv_path = os.path.join(table_dir, out_spmv_prefix + '_' + matrix_name)

with open(time_path, 'w') as time_out:
    time_out.write(matrix_name + ' ' + str(phil_time) + ' ' + str(oski_time) + '\n')

with open(err_path, 'w') as err_out:
    err_out.write(matrix_name + ' ' + str(phil_err) + ' ' + str(phil_err_std) + ' ' + str(oski_err) + ' ' + str(oski_err_std) + '\n')

with open(spmv_path, 'w') as spmv_out:
    spmv_out.write(matrix_name + ' ' + str(phil_spmv) + ' ' + str(phil_spmv_std) + ' ' + str(oski_spmv) + ' ' + str(oski_spmv_std) + '\n')

