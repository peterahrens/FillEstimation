#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH -t 04:00:00
#SBATCH --mail-user=pahrens@mit.edu
#SBATCH --mail-type=ALL
#SBATCH -p lanka-v3

SCRATCH=/data/scratch/pahrens
MATRIX=$SCRATCH/matrix
HOME=$SCRATCH/FillEstimation
DATA=$HOME/data
source env.sh $HOME

#export TACO_CFLAGS="-O3 -ffast-math -std=c99 -fopenmp -funroll-loops"
#export OMP_NUM_THREADS=12
#export DATA_SPMV_PREFIX="numactl -N 1"
#export TACO_TMPDIR=$HOME/taco/tmp$SLURM_ARRAY_TASK_ID

python data_ref.py $MATRIX $DATA lanka12 $SLURM_ARRAY_TASK_ID
