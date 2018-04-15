#!/bin/bash
#SBATCH -p physical
#SBATCH --time=00:59:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=1node1core
#SBATCH -o 1node1core.out

echo "Execution on 1 node with 1 core"

module load Python/3.5.2-goolf-2015a
python ass01.py

