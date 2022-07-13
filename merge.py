# file1 = '/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/merge/job_million_words0_tgt.txt'
# file2 = '/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/job_million_words1_tgt.txt'
from __future__ import unicode_literals

import collections
import codecs
import numpy as np
import random
import os
import time
import argparse
from datetime import date

import logging
logging.basicConfig(level=logging.INFO)

import pdb
import re

def load_sentences(path_src, path_tgt, start_idx=0, search_size=8000,mode="clean"):
	with open(path_src, encoding='UTF-8') as f:
		src_sentences = f.readlines()
	with open(path_tgt, encoding='UTF-8') as f:
		tgt_sentences = f.readlines()
	
	for src in src_sentences:
		if src == "\n":
			src_sentences.remove(src)
	
	for tgt in tgt_sentences:
		if tgt == "\n":
			tgt_sentences.remove(tgt)

	
	orig_path="/home/alta/BLTSpeaking/exp-ytl28/projects/gec-pretrained/exp-t5-written"
	with codecs.open(orig_path+"/lib/gec-train-bpe-written/prep/train.src", encoding='UTF-8') as f:
		src_sentences_orig = f.readlines()
	with codecs.open(orig_path+"/lib/gec-train-bpe-written/prep/train.tgt", encoding='UTF-8') as f:
		tgt_sentences_orig = f.readlines()
	
	assert len(src_sentences) == len(tgt_sentences), \
		'Mismatch src:tgt - {}:{}'.format(len(src_sentences),len(tgt_sentences))

	num_sentences = len(src_sentences)

	if mode=="clean":
		# pdb.set_trace()

		src_sentences = [sentence.replace("\n","") for sentence in src_sentences]
		tgt_sentences = [sentence.replace("\n","") for sentence in tgt_sentences]
		src_sentences_orig = [sentence.replace("\n","") for sentence in src_sentences_orig]
		tgt_sentences_orig = [sentence.replace("\n","") for sentence in tgt_sentences_orig]

		res_src = []
		res_tgt = []


		# print(num_sentences)

		for idx, (src,src_orig, tgt, tgt_orig) in enumerate(zip(src_sentences,src_sentences_orig, tgt_sentences, tgt_sentences_orig)):
			if src.find(src_orig) == -1:
				print(idx)
				pdb.set_trace()
			if tgt.find(tgt_orig) == -1:
				print(idx)
				pdb.set_trace()
			gen = src[len(src_orig):]
			if not bool(re.search(r"[a-zA-Z]", gen)):
				gen = ""
				pdb.set_trace()
			else:
				gen = gen[:-1] + ' .'
				# pdb.set_trace()
			res_src.append(src_orig+gen)
			res_tgt.append(tgt_orig+gen)
			

	elif mode=="sample":
		start_index = start_idx*search_size
		if start_index >= num_sentences:
			return None, None        
		end_index = min(start_index+search_size, num_sentences)
        # pdb.set_trace()
		test_src = src_sentences[start_index:end_index]
		test_tgt = tgt_sentences[start_index:end_index]

		src_seqs = [sentence.strip() for sentence in test_src]
		tgt_seqs = [sentence.strip() for sentence in test_tgt]
		pdb.set_trace()
    
	return res_src, res_tgt



def merge(file1, file2):
    f1 = open(file1, 'a+')
    with open(file2, 'r') as f2:
        f1.write('\n')
        for i in f2:
            f1.write(i)

def sample(file1, file2):
    f1 = open(file1, 'r')
    with open(file2, 'w+') as f2:
        for i in f1[:200]:
            f2.write(i)
            f2.write('\n')

def clean(file):
    with open(file, 'r') as f2:
        if f2:
            print("None")


dir = "/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/merge/"
# file0 = dir+"old_million_words0_src.txt"
# file1 = dir+"old_million_words1_src.txt"
# file2 = dir+"old_million_words2_src.txt"
# file3 = dir+"old_million_words3_src.txt"
# merge(file0, file1)
# merge(file0, file2)
# merge(file0, file3)

# file0 = dir+"old_million_words0_tgt.txt"
# file1 = dir+"old_million_words1_tgt.txt"
# file2 = dir+"old_million_words2_tgt.txt"
# file3 = dir+"old_million_words3_tgt.txt"
# merge(file0, file1)
# merge(file0, file2)
# merge(file0, file3)



src=dir+"old_len5_src.txt"
tgt=dir+"old_len5_tgt.txt"
src_seqs, tgt_seqs = load_sentences(src, tgt, 0, 200,"clean")
# outdir="/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/merge/old_len5_toy"

# with open(outdir+"_src.txt", 'w') as f:
#     for seq in src_seqs:
#         f.write(seq)
#         f.write('\n')
# f.close()


# with open(outdir+"_tgt.txt", 'w') as f:
#     for seq in tgt_seqs:
#         f.write(seq)
#         f.write('\n')
# f.close()

