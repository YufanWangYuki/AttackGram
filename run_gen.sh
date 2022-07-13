#!/bin/bash
#$ -S /bin/bash

source ~/.bashrc
export PATH=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/bin/:$PATH
source activate /home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37
export PYTHONBIN=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37/bin/python3
export PYTHONPATH="${PYTHONPATH}:/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/"

# export OMP_NUM_THREADS=1 # export OMP_NUM_THREADS=1
# export OPENBLAS_NUM_THREADS=1 # export OPENBLAS_NUM_THREADS=1
# export MKL_NUM_THREADS=1 # export MKL_NUM_THREADS=1
# export VECLIB_MAXIMUM_THREADS=1 # export VECLIB_MAXIMUM_THREADS=1
# export NUMEXPR_NUM_THREADS=1 # export NUMEXPR_NUM_THREADS=1

# export CUDA_VISIBLE_DEVICES=$X_SGE_CUDA_DEVICE
export CUDA_VISIBLE_DEVICES=0
echo $CUDA_VISIBLE_DEVICES

# ------------------------ DIR --------------------------
# orig_path=/home/alta/BLTSpeaking/exp-ytl28/projects/gec-pretrained/exp-t5-written 
# train_path_src=$orig_path/lib/gec-train-bpe-written/prep/train.src #3101262
# train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/train.tgt

orig_path=/home/alta/BLTSpeaking/exp-ytl28/projects/lib/gec-train-bpe-written/prep-v2
train_path_src=$orig_path/train.src #2115141
train_path_tgt=$orig_path/train.tgt


# ----------------------- [debug] ---------------------------
# train_path_src=$orig_path/lib/gec-train-bpe-written/prep/dev.src #1929 
# train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/dev.tgt
SGE_TASK_ID=2
# ===================================================================================
word_way=generate
# mkdir /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/$word_way
$PYTHONBIN /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/utils/dataset_generate.py \
    --train_path_src $train_path_src \
	--train_path_tgt $train_path_tgt \
    --log /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/$word_way/new_million_words$SGE_TASK_ID \
    --start $SGE_TASK_ID \
    --search_size 80000 \
    --word_way $word_way

# Run below command to submit this script as an array job
# qsub -cwd -j yes -P esol -l qp=low -o LOGs/run-array-optimal.txt -t 1-400 -l not_host="air113|air112" run_gen.sh

# qsub -cwd -j yes -P esol -l qp=low -o LOGs/run-array-optimal-2.txt -t 101-200 -l not_host="air113|air112" run_gen.sh


# 0 floral
# 1 million stop
# 2 6199190 qsub -cwd -j yes -o 'LOGs/job2.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1
# 3 6199191 qsub -cwd -j yes -o 'LOGs/job3.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1
# 4 6199192 qsub -cwd -j yes -o 'LOGs/job4.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1
# 5 6199193 qsub -cwd -j yes -o 'LOGs/job5.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1
# 6 6199194 stop qsub -cwd -j yes -o 'LOGs/job6.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1


# 0 floral over
# 1 million over
# 6199200 qsub -cwd -j yes -o 'LOGs/new_job2.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1
# 6199201 qsub -cwd -j yes -o 'LOGs/new_job3.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1
# 6199202 qsub -cwd -j yes -o 'LOGs/new_job4.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='*' -l osrel='*' run_gen.sh 1 1

# 2 million
# 3 floral
# 4 million






