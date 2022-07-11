file1 = '/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/merge/job_million_words0_src.txt'
file2 = '/home/alta/BLTSpeaking/exp-yw575/GEC/AttackGram/dataset/generate/job_million_words1_src.txt'

def merge(file1, file2):
    f1 = open(file1, 'a+')
    with open(file2, 'r') as f2:
        f1.write('\n')
        for i in f2:
            f1.write(i)


merge(file1, file2)