from mtranslate import translate


with open('input_en.txt') as f:
    content = f.readlines()
    content = [x.strip() for x in content]

def tran(words):
    tr_words = [translate(word.lower(), 'ro' , 'en' ).encode('ascii','ignore') for word in words]
    return tr_words

print tran(content)