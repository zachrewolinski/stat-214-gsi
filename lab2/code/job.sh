#!/bin/bash

# EXAMPLE USAGE:
# See stat-214-gsi/computing/psc-instructions.md for guidance on how to do this on PSC.
# These are settings for a hypothetical cluster and probably won't work on PSC
# sbatch job.sh configs/default.yaml

#SBATCH --job-name=lab2-autoencoder
#SBATCH --partition=gpu
#SBATCH --gres=gpu:A5000:1
#SBATCH --cpus-per-task=4

python run_autoencoder.py $1