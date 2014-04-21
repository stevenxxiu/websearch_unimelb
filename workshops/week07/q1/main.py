
import math
import os
from collections import Counter
from workshops.lib.store.freq_pair import parse_freq_pairs

def get_background_model(all_probs):
    res = Counter()
    for prob in all_probs:
        res.update(prob)
    return res

def freqs_to_probs(freqs):
    '''
    return the probabilities of the frequencies for each term under MLE
    '''
    res = Counter()
    total_count = sum(freqs.values())
    for term, count in freqs.items():
        res[term] = count/total_count
    return res

def kl_divergence(probs_p, probs_q, probs_bg, lambda_):
    kl_d = 0
    for term in probs_p:
        kl_d += (
                    math.log(probs_p[term]) - math.log((1-lambda_)*probs_q.get(term, 0) + lambda_*probs_bg[term])
                ) * probs_p[term]
    return kl_d

def main():
    data_path = '../../../../data/txt_freq'
    all_freqs = {}
    for filename in os.listdir(data_path):
        all_freqs[filename] = parse_freq_pairs(os.path.join(data_path, filename))
    all_probs = dict((filename, freqs_to_probs(freqs)) for filename, freqs in all_freqs.items())
    probs_bg = get_background_model(all_probs.values())
    file_p = 'sp-AWTEW-freq.dat'
    lambda_ = 0.4
    kls = {}
    for file_q in sorted(all_probs):
        if file_q == file_p:
            continue
        kls[(file_p, file_q)] = kl_divergence(all_probs[file_p], all_probs[file_q], probs_bg, lambda_)
    for (file_p, file_q), kl_value in sorted(kls.items(), key=lambda x: x[1]):
        print('{:<60} {}'.format(
            'D_KL({}||{})'.format(file_p, file_q),
            kl_value
        ))

if __name__ == '__main__':
    main()
