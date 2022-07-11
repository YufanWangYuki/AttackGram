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

# customised
# from utils.misc import check_device
from utils.align_preds import align_data_train, get_sentences_dict

import logging
logging.basicConfig(level=logging.INFO)

import pdb

def load_sentences(path_src, path_tgt, start_idx=0, search_size=8000):
	with codecs.open(path_src, encoding='UTF-8') as f:
		src_sentences = f.readlines()
	with codecs.open(path_tgt, encoding='UTF-8') as f:
		tgt_sentences = f.readlines()
	
	assert len(src_sentences) == len(tgt_sentences), \
		'Mismatch src:tgt - {}:{}'.format(len(src_sentences),len(tgt_sentences))

	num_sentences = len(src_sentences)
	start_index = start_idx*search_size

	if start_index >= num_sentences:
		return None, None

	end_index = min(start_index+search_size, num_sentences)
	pdb.set_trace()
	test_src = src_sentences[start_index:end_index]
	test_tgt = tgt_sentences[start_index:end_index]

	src_seqs = [sentence.strip() for sentence in test_src]
	tgt_seqs = [sentence.strip() for sentence in test_tgt]
    
    

	return src_seqs, tgt_seqs



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

# merge(file1, file2)

src="/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/merge/old_len5_src.txt"
tgt="/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/merge/old_len5_tgt.txt"
load_sentences(src, tgt, 0, 200)

