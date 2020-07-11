from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import logging

from bs4 import BeautifulSoup 

def get_history_by_id_notation(id_notation: str) -> List[Dict[str, Any]]:
    url = 'https://www.onvista.de/etf/ajax/snapshotHistory' # Set destination URL here
    post_fields = {'timeSpan': '1Y', 'codeResolution': '1D', 'idNotation': id_notation}     # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    json_str = urlopen(request).read().decode()
    return json.loads(json_str)

def search_ISIN(isin):
    url = 'https://www.onvista.de/api/header/search?q=' + isin # Set destination URL here

    json_str = urlopen(url).read().decode()
    search_result = json.loads(json_str)
    return search_result['onvista']['results']['asset']

def normalize_string(s: str) -> str:
    return s.lower().replace(" ", "")

def get_exchanges_for_snapshotlink(snapshotlink: str) -> Dict[str, str]:
    """

    """
    page = urlopen(snapshotlink).read().decode()
    soup = BeautifulSoup(page, features="html.parser")

    result = soup.body.find('div', attrs={'id' : 'select-exchange'}).find_all('div', attrs={'class': 'item'})

    exchange_idnotation = {normalize_string(x['data-contributor']): x['data-value'] for x in result}

    return exchange_idnotation


def get_isin_obj(isin: str) -> Dict[str, Any]:
    isin_results = search_ISIN(isin)
    if len(isin_results) < 1:
        raise ValueError(f"No asset found for {isin}")
    if len(isin_results) > 1:
        logging.warn(f"Multiple assets found for {isin}:")
        for r in isin_results:
            logging.warn(r['name'])

    return isin_results[0]

def get_exchanges_for_isin(isin: str) -> List[str]:
    pass


def get_history_by_isin(isin: str, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
    obj = get_isin_obj(isin)
    
    if exchange is None:
        return get_history_by_id_notation(obj['notationid'])
    else:
        exchange_idnotation = get_exchanges_for_snapshotlink(obj['snapshotlink'])
        requested_exchange = normalize_string(exchange)
        if requested_exchange in exchange_idnotation.keys():
            return get_history_by_id_notation(exchange_idnotation[requested_exchange])
        else:
            raise ValueError(f"Requested exchange {exchange} not available. Available exchanges: {exchange_idnotation.keys()}")
