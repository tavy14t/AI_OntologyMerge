from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import unicodedata
import glob
import docx

# Requires internet connection!
results = []


def access_sinonim_site(word):
    try:
        with urlopen('https://dexonline.net/sinonime-%s' % word) as response:
            html = response.read()
            return html
    except Exception:
        return 'bad'


def extract_sinonims(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        raw_sinonims = soup.find(
            "div", attrs={"class": "tip-definitie"}).find('p')
        sinonims = raw_sinonims.getText(separator=u'+')
        sinonims = unicodedata.normalize(
            'NFKD', sinonims).encode('ascii', 'ignore')
    except Exception:
        sinonims = ""
    return sinonims


def proccess_sinonims(sinonims):
    sinonims = sinonims.decode('UTF-8')
    sino = re.sub("[\(\[].*?[\)\]]", "", sinonims)
    sino = re.sub(" ", "", sino)
    sino = re.sub("s.", "", sino, 1)
    sino = re.sub("pl.", "", sino, 1)
    sino = re.sub("\.", "", sino)
    sino = re.sub("[;0-9=]", "", sino)
    processed_sinonims = []
    sino = sino.split("+")
    for x in sino:
        if x is not "":
            y = x.split(",")
            processed_sinonims = processed_sinonims + y
    # del cuv original
    try:
        processed_sinonims.pop(0)
    except Exception:
        pass
    # ========
    good_sinonims = []
    for x in processed_sinonims:
        if x is not "" and x is not "v":
            good_sinonims.append(x)
    return good_sinonims


def get_sinonim_list(l1, l2):
    l3 = []
    for word in l1:
        site = access_sinonim_site(word)
        if site is not "bad":
            raw_sino = extract_sinonims(site)
            sino = proccess_sinonims(raw_sino)
            for word2 in l2:
                for i in range(0, len(sino)):
                    if word2 == sino[i]:
                        l3.append((word, "is_synonymous", word2))
    return l3


# Exemplu:
print(get_sinonim_list(["briceag", "fericit"], ["norocit", "brisca"]))
