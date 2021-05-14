import random

articles = ['a', 'the', 'of', 'an']
nouns = ['cat', 'dog', 'money', 'honey', 'man', 'woman']
verbs = ['sang', 'ran', 'spent', 'jumped', 'checked']
adverbs = ['loudly', 'quietly', 'well', 'badly']


def random_word(seq):
    return random.choice(seq)


for _ in [1, 2, 3, 4, 5]:
    sentecne = [random_word(articles), random_word(nouns), random_word(verbs)]
    if random.randint(0, 1):
        pass
    else:
        sentecne.append(random_word(adverbs))
    print(*sentecne)
