import requests
from lxml import html
from unidecode import unidecode


def get_definitions(word):
    DEX_BASE_URL = 'https://dexonline.ro'
    DEX_API_URL_FORMAT = '{}/{}'.format(DEX_BASE_URL, 'definitie/{}/json')

    dex_api_url = DEX_API_URL_FORMAT.format(word)
    dex_api_request = requests.get(dex_api_url)

    dex_raw_response = dex_api_request.json()
    dex_raw_definitions = dex_raw_response['definitions']
    dex_definitions = []

    for dex_raw_definition in dex_raw_definitions:
        dex_definition_html_rep = dex_raw_definition['htmlRep']
        html_fragments = html.fragments_fromstring(dex_definition_html_rep)
        root = html.Element('root')
        for html_fragment in html_fragments:
            root.append(html_fragment)

        dex_definition_text = root.text_content()
        dex_definition_text = unidecode(dex_definition_text)
        dex_definitions.append(dex_definition_text)
    return(dex_definitions[0].split(';')[0])


print(get_definitions('avion'))
