#!/bin/bash
#$ -S /bin/bash


source ~/.bashrc
conda activate conda_env36

export OMP_NUM_THREADS=1 # export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1 # export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1 # export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 # export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 # export NUMEXPR_NUM_THREADS=1


python /home/alta/BLTSpeaking/exp-vr313/GEC/TunedGramformerAttack/uni_attack_evade_perplexity.py /home/alta/CLC/LNRC/exams/FCEsplit-public/v3/fce-public.train16.inc /home/alta/BLTSpeaking/exp-yw575/GEC/NoiseGram/models/v003/volta_Gaussian-adversarial_mul_1.0_0.1_256_8/checkpoints-combine/combine/model.pt /home/alta/BLTSpeaking/grd-graphemic-vr313/speech_processing/adversarial_attack/word2vec/test_words.txt /home/alta/BLTSpeaking/exp-yw575/GEC/NoiseGram/models/v003/volta_Gaussian-adversarial_mul_1.0_0.1_256_8/universal_attack_logs/evade_perp_beam1/k1/words$SGE_TASK_ID.txt --prev_attack= --search_size=200 --start=$SGE_TASK_ID --num_points=500 --perp_thresh=243

# Run below command to submit this script as an array job
# qsub -cwd -j yes -P esol -l qp=low -o LOGs/v003/run-array-evade_perp.txt -t 1-224 -l not_host="air113|air112" run_search_evade_perp.sh
