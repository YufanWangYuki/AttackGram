# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unicodedata import digit

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
import csv
from tqdm import tqdm

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

def count_sentences(path_src, path_tgt, word_way='generate',start_idx=0, search_size=8000):
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
	src_seqs = [sentence.strip() for sentence in src_sentences]
	tgt_seqs = [sentence.strip() for sentence in tgt_sentences]

	full_num = 0
	alpha_num = 0
	digit_num = 0
	comma_num = 0
	colon_num = 0
	others = {}
	others['Empty'] = 0
	for seq in tqdm(src_seqs):
		if len(seq) == 0:
			others['Empty'] += 1
		elif seq[-1] == '.':
			full_num += 1
		elif seq[-1].isalpha():
			alpha_num += 1
		elif seq[-1].isdigit():
			digit_num += 1
		elif seq[-1] == ',':
			comma_num += 1
		elif seq[-1] == ';':
			colon_num += 1
		else:
			if seq[-1] not in others:
				others[seq[-1]] = 1
			else:
				others[seq[-1]] += 1
	others['full stop'] = full_num
	others['alpha'] = alpha_num
	others['digit'] = digit_num
	others['comma'] = comma_num
	others['colon'] = colon_num
	return others

if __name__ == "__main__":
	# Get command line arguments
	commandLineParser = argparse.ArgumentParser()
	commandLineParser.add_argument('--train_path_src', type=str, required=True, help='train src dir')
	commandLineParser.add_argument('--train_path_tgt', type=str, required=True, help='train tgt dir')
	commandLineParser.add_argument('--log', type=str, help='Specify txt file to log iteratively better words')
	args = commandLineParser.parse_args()

	dict = count_sentences(args.train_path_src, args.train_path_tgt)
	
	with open(args.log+'.csv', 'w') as f:
		writer = csv.writer(f)
		for k, v in dict.items():
			writer.writerow([k, v])



