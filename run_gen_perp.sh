#!/bin/bash
#$ -S /bin/bash
export CUDA_VISIBLE_DEVICES=$X_SGE_CUDA_DEVICE
# export CUDA_VISIBLE_DEVICES=0
echo $CUDA_VISIBLE_DEVICES

# export PATH=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/bin/:$PATH
source ~/.bashrc
# conda activate /home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37
conda activate gec37
# export PYTHONBIN=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37/bin/python3
# export PYTHONPATH="${PYTHONPATH}:/home/alta/BLTSpeaking/exp-yw575/GEC/NoiseGram/"

# export CUDA_VISIBLE_DEVICES=0
# echo $CUDA_VISIBLE_DEVICES

export OMP_NUM_THREADS=1 # export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1 # export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1 # export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 # export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 # export NUMEXPR_NUM_THREADS=1


# 44928 chutzpah ii bibb en fyi
# chutzpah vb ditka 0.4290416971470373
# chutzpah ii bibb en 
SGE_TASK_ID=0
length=4
num_points=100
python /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/run_gen_perp.py \
    /home/alta/CLC/LNRC/exams/FCEsplit-public/v3/fce-public.train16.inc \
    /home/alta/BLTSpeaking/exp-ytl28/projects/gec-pretrained/exp-t5-written/models/v001/checkpoints-combine/combine/ \
    /home/alta/BLTSpeaking/exp-yw575/GEC/NoiseGram/LOGs/best_words/perp_vocab.txt \
    /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/random_valid/${length}_${num_points}_${SGE_TASK_ID}.txt \
    --length=5 \
    --num_points=100 \
    --perp_thresh=243 \
    --search_size=200
# qsub -cwd -j yes -o 'LOGs/valid_perp_k4.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' train.sh 1 1