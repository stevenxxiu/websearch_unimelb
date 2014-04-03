
def cosine_similarity(weight_dict_1, weight_dict_2):
    '''
    assumes that both weight_dict_1 and weight_dict_2 are normalized
    '''
    score = 0
    for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
        score += weight_dict_1[term]*weight_dict_2[term]
    return score
