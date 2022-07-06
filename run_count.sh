#!/bin/bash
#$ -S /bin/bash


echo export PATH=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/bin/:$PATH
source activate /home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37
export PYTHONBIN=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37/bin/python3
export PYTHONPATH="${PYTHONPATH}:/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/"

# export CUDA_VISIBLE_DEVICES=$X_SGE_CUDA_DEVICE
export CUDA_VISIBLE_DEVICES=0
echo $CUDA_VISIBLE_DEVICES

# ------------------------ DIR --------------------------
# orig_path=/home/alta/BLTSpeaking/exp-ytl28/projects/gec-pretrained/exp-t5-written 
# train_path_src=$orig_path/lib/gec-train-bpe-written/prep/train.src #3101262
# train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/train.tgt
orig_path=/home/alta/BLTSpeaking/exp-ytl28/projects/lib/gec-train-bpe-written/prep-v2
train_path_src=$orig_path/train.src
train_path_tgt=$orig_path/train.tgt

# ----------------------- [debug] ---------------------------
# train_path_src=$orig_path/lib/gec-train-bpe-written/prep/dev.src #1929 
# train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/dev.tgt
# ===================================================================================
$PYTHONBIN /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/utils/dataset_count.py \
    --train_path_src $train_path_src \
	--train_path_tgt $train_path_tgt \
    --log /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/LOGs/count_test


