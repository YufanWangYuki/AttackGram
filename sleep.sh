#!/bin/bash
#$ -S /bin/bash
# export CUDA_VISIBLE_DEVICES=$X_SGE_CUDA_DEVICE
export CUDA_VISIBLE_DEVICES=0
echo $CUDA_VISIBLE_DEVICES

# export PATH=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/bin/:$PATH
source ~/.bashrc
# conda activate /home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37
conda activate gec37

python /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/sleep.py