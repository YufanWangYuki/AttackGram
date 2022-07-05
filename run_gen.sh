#!/bin/bash
#$ -S /bin/bash


echo export PATH=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/bin/:$PATH
source activate /home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37
export PYTHONBIN=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37/bin/python3
export PYTHONPATH="${PYTHONPATH}:/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/"

export OMP_NUM_THREADS=1 # export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1 # export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1 # export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 # export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 # export NUMEXPR_NUM_THREADS=1

# ------------------------ DIR --------------------------
orig_path=/home/alta/BLTSpeaking/exp-ytl28/projects/gec-pretrained/exp-t5-written 
train_path_src=$orig_path/lib/gec-train-bpe-written/prep/train.src #3101262
train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/train.tgt

# ----------------------- [debug] ---------------------------
# train_path_src=$orig_path/lib/gec-train-bpe-written/prep/dev.src #1929 
# train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/dev.tgt

# ===================================================================================
word_way=generate
# mkdir /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/$word_way
$PYTHONBIN /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/utils/dataset_generate.py \
    --train_path_src $train_path_src \
	--train_path_tgt $train_path_tgt \
    --log /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/$word_way/tmp_words$SGE_TASK_ID \
    --start 100 \
    --search_size 1000 \
    --word_way $word_way

# Run below command to submit this script as an array job
# qsub -cwd -j yes -P esol -l qp=low -o LOGs/run-array-optimal.txt -t 1-400 -l not_host="air113|air112" run_gen.sh

# qsub -cwd -j yes -P esol -l qp=low -o LOGs/run-array-optimal-2.txt -t 101-200 -l not_host="air113|air112" run_gen.sh
