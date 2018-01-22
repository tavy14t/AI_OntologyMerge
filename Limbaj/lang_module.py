
from googletrans import Translator
import requests
from bs4 import BeautifulSoup

def compute_name_score(str1, str2):
    # Names shorter than 3 letters are ignored
    if len(str1) < 3 or len(str2) < 3:
        return 0

    # Working with lowercase characters only
    str1 = str1.lower()
    str2 = str2.lower()

    # Split composite-words (if there are any) and calculate max score
    str1 = str1.replace('-', ' ')
    str2 = str2.replace('-', ' ')
    words1 = str1.split()
    words2 = str2.split()

    max_score = 0
    for word1 in words1:
        for word2 in words2:
            score = letter_match_length(word1, word2)
            if score > max_score:
                max_score = score

    equal_len_score = 0
    if len(str1) == len(str2):
        equal_len_score = 20
    elif max_score > 1:
        equal_len_score = 10
    return max_score**2 + equal_len_score


def compute_definition_score(str1, str2):
    def1 = get_definition(str1)
    def2 = get_definition(str2)
    def1 = def1.split()
    def2 = def2.split()
    def1 = remove_morph_words(def1)
    def2 = remove_morph_words(def2)

    reliability = 0
    for x in def1:
        for y in def2:
            if x == y:
                reliability = reliability + 1

    strength = reliability / min(len(def1), len(def2))
    return strength * reliability


def letter_match_length(str1, str2):
    i = len(str1) - 1
    j = len(str2) - 1
    length = 0
    while i >= 0 and j >= 0:
        if str1[i] == str2[j]:
            length = length + 1
        else:
            return length
        i = i - 1
        j = j - 1
    return length


def get_definition(term):
    translator = Translator()
    translation = translator.translate(term, dest='en')
    translation = remove_morph_words(translation.text.split())

    response = requests.get('https://www.vocabulary.com/dictionary/' + translation[0])
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        definition = soup.find('h3', attrs={'class': 'definition'})
        definition = definition.text.strip()
        definition = ' '.join(definition[1:].split())
    except:
        return '[NONE]'

    output = ''
    for c in definition:
        if c.isalpha() or c.isspace():
            output = output + c
    return output


def remove_morph_words(wordlist):
    for i in range(0, len(wordlist)):
        if wordlist[i].endswith('es'):
            wordlist[i] = wordlist[i][:-2]
        elif wordlist[i].endswith('ds') or wordlist[i].endswith('ts'):
            wordlist[i] = wordlist[i][:-1]

    output = []
    for word in wordlist:
        if word != 'a' and word != 'by' and word != 'the' and word != 'as' and word != 'an'\
            and word != 'is' and word != 'of' and word != 'in' and word != 'and':
                output.append(word)
    return output

def get_match_score(str1, str2):
    namescore = compute_name_score(str1, str2)
    defscore = compute_definition_score(str1, str2)
    if namescore == 0:
        namescore = 1
    if defscore == 0:
        defscore = 1
    return namescore**(1/2) * defscore *2

def get_synonymus(l1,l2):
    l=[]
    for i in  l1:
        for j in l2:
            if (get_match_score(i,j))>= 12:
                l.append((i,"is_synonymous",j))
    return l


#Exemplu:

#l1 = ["vesel","prieten"]
#l2 = ["amic","trist"]
#print(get_synonymus(l1,l2))
