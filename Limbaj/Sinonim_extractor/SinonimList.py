import urllib2
from bs4 import BeautifulSoup
import re
import unicodedata

#!!! Requires internet connection !!!
def access_sinonim_site(word):
    try:
        response = urllib2.urlopen('https://dexonline.net/sinonime-'+word)
        html = response.read()
        return html
    except:
        return 'bad'

def extract_sinonims(html):
    soup = BeautifulSoup(html,'html.parser')
    try:
        raw_sinonims=soup.find("div",attrs={"class":"tip-definitie"}).find('p')
        sinonims = raw_sinonims.getText(separator=u'+')
        sinonims = unicodedata.normalize('NFKD', sinonims).encode('ascii', 'ignore')
    except:
        sinonims=""
    return sinonims

def proccess_sinonims(sinonims):
    sino=re.sub("[\(\[].*?[\)\]]", "", sinonims)
    sino=re.sub(" ","",sino)
    sino=re.sub("s.","",sino,1)
    sino=re.sub("pl.","",sino,1)
    sino=re.sub("\.","",sino)
    sino=re.sub("[;0-9=]","",sino)
    processed_sinonims=[]
    sino=sino.split("+")
    for x in sino:
        if x is not "":
            y=x.split(",")
            processed_sinonims= processed_sinonims+y
    # del cuv original
    try:
        processed_sinonims.pop(0)
    except:
        pass
    # ========
    good_sinonims=[]
    for x in processed_sinonims:
        if x is not "" and x is not "v":
            good_sinonims.append(x)
    return good_sinonims

def get_list(l1,l2):
	l3=[]
	for word in l1:
		site=access_sinonim_site(word)
		if site is "bad":
			return []
		else:
			raw_sino=extract_sinonims(site)
			sino=proccess_sinonims(raw_sino)
			for word2 in l2:
				for i in range(0,len(sino)):
					if word2==sino[i]:
						if (word+","+word2)not in l3 and (word2+","+word) not in l3:
							l3.append(word+","+ word2)
	return l3;



#Exemplu:
print(get_list(["briceag", "fericit"],["norocit","brisca"]))


