'''
At input expect a SOURCE, REF and PRED file:

ID1 text1
ID2 text2
.
.
.

Output the errant edit type distribution; for each edit type give the following:

Ref count, Pred Total Count, Pred Correct Count, Pred Inserted Count, Pred Deleted Count 

'''
import sys
import os
import argparse
from utils.gec_tools import return_edits
from collections import defaultdict
from utils.align_preds import align_data_pred, get_sentences_dict
from utils.uni_attack import concatenate
from statistics import mean, stdev
import time

def update_edit_types(ref_edits, pred_edits, ref_count, pred_total, pred_correct, pred_insert, pred_del):
    '''
    Collect all edit type information
    '''
    ref_edit_strs = [e.o_str+' -> '+e.c_str for e in ref_edits]
    pred_edit_strs = [e.o_str+' -> '+e.c_str for e in pred_edits]

    for e in ref_edits:
        ref_count[e.type] += 1

        curr_str = e.o_str+' -> '+e.c_str
        if curr_str not in pred_edit_strs:
            pred_del[e.type] += 1
    
    for e in pred_edits:
        pred_total[e.type] += 1
    
        curr_str = e.o_str+' -> '+e.c_str
        if curr_str in ref_edit_strs:
            pred_correct[e.type] += 1
        else:
            pred_insert[e.type] += 1
    
def get_edits_by_part(original_sentence, attack_edits):
    '''
    Determine how many attack edits in which part of attacked sentence
    '''

    edit_strs = [e.o_str for e in attack_edits]
    orig = 0
    adv = 0
    for e_str in edit_strs:
        if original_sentence.find(e_str) == -1:
            adv+=1
        else:
            orig+=1
    return orig, adv


if __name__ == "__main__":

    # Get command line arguments
    commandLineParser = argparse.ArgumentParser()
    commandLineParser.add_argument('--SOURCE', type=str, help='Path to source data')
    commandLineParser.add_argument('--REF', type=str, help='Path to correct reference data')
    commandLineParser.add_argument('--PRED', type=str, help='Path to prediction data')
    commandLineParser.add_argument('--OUT', type=str, help='Path to save edit type information')
    commandLineParser.add_argument('--phrase', type=str, default='', help='Universal adversarial phrase')
    commandLineParser.add_argument('--delim', type=str, default='', help='concatenation delimiter')
    args = commandLineParser.parse_args()

    # Save the command run
    if not os.path.isdir('CMDs'):
        os.mkdir('CMDs')
    with open('CMDs/eval_error_dist.cmd', 'a') as f:
        f.write(' '.join(sys.argv)+'\n') 

    # Get sentences and align
    inc_id2text = get_sentences_dict(args.SOURCE)
    pred_id2text = get_sentences_dict(args.PRED)
    corr_id2text = get_sentences_dict(args.REF)
    inc_sens, pred_sens, corr_sens = align_data_pred(inc_id2text, pred_id2text, corr_id2text)

    inc_sens = [s.rstrip('\n') for s in inc_sens]
    pred_sens = [s.rstrip('\n') for s in pred_sens]
    corr_sens = [s.rstrip('\n') for s in corr_sens]


    # Get the edit types dicts
    ref_count = defaultdict(int)
    pred_total = defaultdict(int)
    pred_correct = defaultdict(int)
    pred_insert = defaultdict(int)
    pred_del = defaultdict(int)

    # Get fraction of samples with no edits
    num_samples_no_edits = 0

    # count of edits per part
    original_part_count = [] # for adv phrase, count of edits in non adv-part
    adv_part_count = [] # for adv phrase, count of edits in adv-part

    for i, (s, r, p) in enumerate(zip(inc_sens, corr_sens, pred_sens)):
        print(f'On {i}/{len(inc_sens)}')
        ref_edits = return_edits(s, r)

        s_with_attack = s[:]
        if args.phrase != '':
            attack_phrase = args.phrase + '.'
            s_with_attack = concatenate(s, attack_phrase, delim=args.delim)
        pred_edits = return_edits(s_with_attack, p)
        # import pdb; pdb.set_trace()
        if len(pred_edits) == 0:
            num_samples_no_edits += 1
        update_edit_types(ref_edits, pred_edits, ref_count, pred_total, pred_correct, pred_insert, pred_del)

        # Get edits by part of sentence
        original_part, adv_part = get_edits_by_part(s, pred_edits)
        original_part_count.append(original_part)
        adv_part_count.append(adv_part)
    
    # Get fraction of samples with no edits
    frac_no_edits = num_samples_no_edits/len(inc_sens)

    # Get average number of edits per original and adv part of sentence
    orig_mean = mean(original_part_count)
    orig_std = stdev(original_part_count)
    adv_mean = mean(adv_part_count)
    adv_std = stdev(adv_part_count)
    
    # Save edit type distribution to file
    texts = ['Type Ref-Count Pred-Total Pred-Correct Pred-Insert Pred-Delete']
    for edit_type in sorted(list(ref_count.keys())):
        texts.append(f'\n{edit_type} {ref_count[edit_type]} {pred_total[edit_type]} {pred_correct[edit_type]} {pred_insert[edit_type]} {pred_del[edit_type]}')
    texts.append(f'\n\nSum {sum(ref_count.values())} {sum(pred_total.values())} {sum(pred_correct.values())} {sum(pred_insert.values())} {sum(pred_del.values())}')
    texts.append(f'\n\nFraction of Samples with no edits from source to prediction: {frac_no_edits}')
    texts.append(f'\nOriginal Part Edits:\tMean: {orig_mean}\t Std: {orig_std}')
    texts.append(f'\nAdv Part Edits:\tMean: {adv_mean}\t Std: {adv_std}')
    with open(args.OUT, 'w') as f:
            f.writelines(texts)
    