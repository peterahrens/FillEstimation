#!/bin/bash -l

#SBATCH -N 1         #Use 2 nodes
#SBATCH -t 02:00:00
#SBATCH --mail-user=pahrens@mit.edu
#SBATCH --mail-type=ALL
#SBATCH --array=0-31
#SBATCH -p regular   #Submit to the regular 'partition'
#SBATCH -L SCRATCH   #Job requires $SCRATCH file system
#SBATCH -C haswell   #Use KNL nodes in quad cache format (default, recommended)

module load python
python generate_spmv_times.py $SCRATCH/fill_estimation $SCRATCH/fill_estimation/haswell $SLURM_ARRAY_TASK_ID