from mtranslate import translate


with open('input_ro.txt') as f:
    content = f.readlines()
    content = [x.strip() for x in content]

def tran(words):
    tr_words = [translate(word.lower(), 'en' , 'ro' ).encode('ascii','ignore') for word in words]
    return tr_words

print tran(content)