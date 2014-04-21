
from collections import Counter

def parse_freq_pairs(path):
    freqs = Counter()
    with open(path, 'r') as sr:
        for line in sr:
            freq, term = line.split(maxsplit=2)
            freqs[term] = int(freq)
    return freqs
