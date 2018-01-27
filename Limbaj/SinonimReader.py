import urllib2
import BeautifulSoup
import re
import unicodedata

#  !!! Requires internet connection !!!


def access_sinonim_site(word):
    try:
        response = urllib2.urlopen('https://dexonline.net/sinonime-%s' % word)
        html = response.read()
        return html
    except Exception:
        return 'bad'


def extract_sinonims(html):
    soup = BeautifulSoup.BeautifulSoup(html)
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


def get_sinonims(word, how_many):
    site = access_sinonim_site(word)

    if site is "bad":
        return []
    else:
        raw_sino = extract_sinonims(site)
        sino = proccess_sinonims(raw_sino)
        if how_many > 0:
            if how_many < len(sino):
                sinonims = []
                for i in range(0, how_many):
                    sinonims.append(sino[i])
                return sinonims
            else:
                return sino
        else:
            return []


# Exemplu:
print(get_sinonims('briceag', 2))
