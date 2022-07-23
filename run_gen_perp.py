'''
Perform concatenation adversarial attack on 
GEC system, with aim of finding universal adversarial phrase
that minimises average number of edits between original and 
predicted gec sentence and ensures attack phrase keeps perplexity below detection threshold.
'''
import sys
import os
import argparse
import torch
from utils.gec_tools import get_sentences, correct, count_edits
from Seq2seq import Seq2seq
from eval_uni_attack import set_seeds
import json
from datetime import date
from uni_attack import get_avg
from perplexity import perplexity
from statistics import mean
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import copy
from modules.checkpoint import Checkpoint
import pdb
from tqdm import tqdm
import random 

perp_tokenizer = GPT2TokenizerFast.from_pretrained('distilgpt2')
perp_model = GPT2LMHeadModel.from_pretrained('distilgpt2')

def is_perp_less_than_thresh(sentences, attack_phrase, thresh):
    '''
        Return True if the average dataset perplexity is less than threshold
    '''
    perps = []
    for sent in sentences:
        sent = sent + ' ' + attack_phrase
        try:
            perp = perplexity(sent, perp_tokenizer, perp_model)
            perps.append(min(perp, 1000))
        except:
            continue
        # import pdb; pdb.set_trace()
    avg_perp = mean(perps)
    if avg_perp < thresh:
        return True
    return False

if __name__ == "__main__":

    # Get command line arguments
    commandLineParser = argparse.ArgumentParser()
    commandLineParser.add_argument('IN', type=str, help='Path to input data')
    commandLineParser.add_argument('MODEL', type=str, help='Path to Gramformer model')
    commandLineParser.add_argument('VOCAB', type=str, help='ASR vocab file')
    commandLineParser.add_argument('LOG', type=str, help='Specify txt file to log iteratively better words')
    commandLineParser.add_argument('--length', type=int, default='', help='attack phrase length')
    commandLineParser.add_argument('--num_points', type=int, default=1000, help='Number of training data points to consider')
    # commandLineParser.add_argument('--search_size', type=int, default=400, help='Number of words to check')
    # commandLineParser.add_argument('--start', type=int, default=0, help='Vocab batch number')
    commandLineParser.add_argument('--perp_thresh', type=float, default=0, help='Perplexity Detector threshold')
    commandLineParser.add_argument('--seed', type=int, default=1, help='reproducibility')
    args = commandLineParser.parse_args()

    # Save the command run
    if not os.path.isdir('CMDs'):
        os.mkdir('CMDs')
    with open('CMDs/run_gen_perp.cmd', 'a') as f:
        f.write(' '.join(sys.argv)+'\n')
    
    set_seeds(args.seed)

    device = torch.device('cpu')
    latest_checkpoint_path = args.MODEL
    resume_checkpoint = Checkpoint.load(latest_checkpoint_path)
    model = resume_checkpoint.model.to(device)
    model.eval()

    # Load input sentences
    _, sentences = get_sentences(args.IN, num=args.num_points)

    # Get list of words to try
    test_words = []
    with open(args.VOCAB, 'r') as f:
        lines = f.readlines()
    for line in lines[2:]:
        word = line.strip()
        test_words.append(word)
    print(len(test_words))

    # Initialise empty log file
    with open(args.LOG, 'w') as f:
        f.write("Logged on "+ str(date.today()))

    cnt = 0
    res = []
    while cnt < args.search_size:
        gen = []
        for i in range(args.length):
            w_id = random.randint(0, len(test_words)-1)
            gen.append(test_words[w_id])
        attack_phrase = (" ").join(gen)
        if not is_perp_less_than_thresh(sentences, attack_phrase, args.perp_thresh):
            continue
        else:
            edits_avg = get_avg(model, sentences, attack_phrase)
            if edits_avg < 1:
                pdb.set_trace()
                res.append(gen)
                cnt += 1
                with open(args.LOG, 'a') as f:
                    out = '\n'+res+" "+str(edits_avg)
                    f.write(out)
