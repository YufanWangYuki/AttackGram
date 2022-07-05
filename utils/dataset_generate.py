# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import torch
import torch.utils.data
import collections
import codecs
import numpy as np
import random
import os
import time
import argparse
from datetime import date

# huggingface api
from transformers import T5Tokenizer
from transformers import AutoTokenizer

# customised
# from utils.misc import check_device
from utils.align_preds import align_data_train, get_sentences_dict
from models.data_helpers import add_words_seq

import logging
logging.basicConfig(level=logging.INFO)

import pdb

def load_sentences(path_src, path_tgt, word_way='generate',start_idx=0, search_size=8000):
	if 'fce' in path_src:
		# FCE
		inc_id2text = get_sentences_dict(path_src)
		corr_id2text = get_sentences_dict(path_tgt)
		src_sentences, tgt_sentences = align_data_train(inc_id2text, corr_id2text)
		# pdb.set_trace()
	else:
		with codecs.open(path_src, encoding='UTF-8') as f:
			src_sentences = f.readlines()
		with codecs.open(path_tgt, encoding='UTF-8') as f:
			tgt_sentences = f.readlines()
	
	assert len(src_sentences) == len(tgt_sentences), \
		'Mismatch src:tgt - {}:{}'.format(len(src_sentences),len(tgt_sentences))

	num_sentences = len(src_sentences)
	start_index = start_idx*search_size
	end_index = min(start_index+search_size, num_sentences)
	test_src = src_sentences[start_index:end_index]
	test_tgt = tgt_sentences[start_index:end_index]

	src_seqs = [sentence.strip() for sentence in test_src]
	tgt_seqs = [sentence.strip() for sentence in test_tgt]

	# pdb.set_trace()
	start = time.time()
	src_seqs, tgt_seqs = add_words_seq(src_seqs, tgt_seqs, length=10, way=word_way)
	end = time.time()
	print(end - start)
	return src_seqs, tgt_seqs

if __name__ == "__main__":
	# Get command line arguments
	commandLineParser = argparse.ArgumentParser()
	commandLineParser.add_argument('--train_path_src', type=str, required=True, help='train src dir')
	commandLineParser.add_argument('--train_path_tgt', type=str, required=True, help='train tgt dir')
	commandLineParser.add_argument('--log', type=str, help='Specify txt file to log iteratively better words')
	commandLineParser.add_argument('--search_size', type=int, default=400, help='Number of words to check')
	commandLineParser.add_argument('--start', type=int, default=0, help='Vocab batch number')
	commandLineParser.add_argument('--word_way', type=str, default='generate',help='way to generate words')
	args = commandLineParser.parse_args()

	src_seqs, tgt_seqs = load_sentences(args.train_path_src, args.train_path_tgt, args.word_way, args.start, args.search_size)

	# Initialise empty log file
	with open(args.log, 'w') as f:
		f.write("Logged on "+ str(date.today()))
	
	for seq in src_seqs:
		with open(args.log, 'a') as f:
			f.write(seq)



