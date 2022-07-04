#!/bin/bash
#$ -S /bin/bash

echo $HOSTNAME
unset LD_PRELOAD
# export PATH=/home/alta/BLTSpeaking/exp-ytl28/env/anaconda3/bin/:$PATH
echo export PATH=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/bin/:$PATH


export CUDA_VISIBLE_DEVICES=$X_SGE_CUDA_DEVICE
# export CUDA_VISIBLE_DEVICES=0
echo $CUDA_VISIBLE_DEVICES

# python 3.7
# pytorch 1.5
# source activate /home/alta/BLTSpeaking/exp-ytl28/env/anaconda3/envs/py38-pt15-cuda10
# export PYTHONBIN=/home/alta/BLTSpeaking/exp-ytl28/env/anaconda3/envs/py38-pt15-cuda10/bin/python3
source activate /home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37
export PYTHONBIN=/home/alta/BLTSpeaking/exp-yw575/env/anaconda3/envs/gec37/bin/python3

# ===================================================================================
# ------------------------ DIR --------------------------
orig_path=/home/alta/BLTSpeaking/exp-ytl28/projects/gec-pretrained/exp-t5-written
train_path_src=$orig_path/lib/gec-train-bpe-written/prep/train.src
train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/train.tgt
dev_path_src=$orig_path/lib/gec-train-bpe-written/prep/dev.src
dev_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/dev.tgt

max_src_len=64
max_tgt_len=64

# ------------------------ TRAIN --------------------------
# [SCHEDULE 1]
# lr_init=0.00001
# lr_peak=0.0007
# lr_warmup_steps=4000

# [SCHEDULE 2] - slower warmup for tuned models
lr_init=0.00001
lr_peak=0.0005
lr_warmup_steps=4000

grab_memory='True'
random_seed=25

# [inactive when dev not given]
max_count_no_improve=30
# max_count_no_improve=10
max_count_num_rollback=0 # 0:no roll back no lr reduce
keep_num=5

# --------------
batch_size=256
# minibatch_split=2 #8 for million
# minibatch_split=8 #8 for million
minibatch_split=8 #8 for million
num_epochs=100

checkpoint_every=5000 # ~10k if 2M, batch - 256
print_every=1000

grab_memory='False'
loaddir='None'
load_mode='null' # 'resume' | 'restart' | 'null'

# ----------------------- [debug] ---------------------------
# train_path_src=$orig_path/lib/gec-train-bpe-written/prep/dev.src
# train_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/dev.tgt
# dev_path_src=$orig_path/lib/gec-train-bpe-written/prep/toy.src
# dev_path_tgt=$orig_path/lib/gec-train-bpe-written/prep/toy.tgt
# # # num_epochs=2
# minibatch_split=2
# batch_size=4
# checkpoint_every=100
# print_every=2

# ----------------------- [noise] ---------------------------
# ntype=Gaussian-adversarial #Gaussian, Bernoulli, Gaussian-adversarial, Adversarial
# nway=add
# mean=0.0
# weight=1000
# alpha=100000000
# decay=0.1
# savedir=models/v005/volta_${ntype}_${nway}_${mean}_${weight}_${alpha}_${decay}_${batch_size}_${minibatch_split}/
noise=0
word_way=generate
savedir=models/$word_way/${batch_size}_${minibatch_split}_v2_full/
# ===================================================================================
$PYTHONBIN /home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/train.py \
	--train_path_src $train_path_src \
	--train_path_tgt $train_path_tgt \
	--dev_path_src $dev_path_src \
	--dev_path_tgt $dev_path_tgt \
	--max_src_len $max_src_len \
	--max_tgt_len $max_tgt_len \
	\
	--lr_peak $lr_peak \
	--lr_init $lr_init \
	--lr_warmup_steps $lr_warmup_steps \
	\
	--batch_size $batch_size \
	--minibatch_split $minibatch_split \
	--num_epochs $num_epochs \
	\
	--load $loaddir \
	--load_mode $load_mode \
	--save $savedir \
	\
	--random_seed $random_seed \
	--max_grad_norm 1.0 \
	--checkpoint_every $checkpoint_every \
	--print_every $print_every \
	--max_count_no_improve $max_count_no_improve \
	--max_count_num_rollback $max_count_num_rollback \
	--keep_num $keep_num \
	--grab_memory $grab_memory \
	--use_gpu True \
	--gpu_id $CUDA_VISIBLE_DEVICES \
	--noise $noise \
	--word_way $word_way
	# --ntype $ntype \
	# --nway $nway \
	# --mean $mean \
	# --weight $weight \
	# --alpha $alpha

# qsub -cwd -j yes -o 'LOGs/generate_v1.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='volta' -l osrel='*' train.sh 1 1
# qsub -cwd -j yes -o 'LOGs/generate_v1_full.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='volta' -l osrel='*' train.sh 1 1

# qsub -cwd -j yes -o 'LOGs/generate_v1_test.log' -P esol -l hostname='*' -l qp=cuda-low -l gpuclass='volta' -l osrel='*' train.sh 1 1