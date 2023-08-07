import colorama
from colorama import Fore
from serpapi import GoogleSearch
import fuckit

from consts import SERP_API_KEY, GLOBAL_HL, GLOBAL_GL, GLOBAL_LOCATION
import consts

colorama.init()


def get_serp_query_result(query: str, n: int = 1, engine: str = 'GoogleSearch') -> list:
    search = []

    print(Fore.LIGHTRED_EX + "\nUsing SerpAPI: " + Fore.RESET + f"{query}, {n} results, {engine} engine;")

    if engine == 'GoogleSearch':
        params = {
            "q": query,
            "location": GLOBAL_LOCATION,
            "hl": GLOBAL_HL,
            "gl": GLOBAL_GL,
            "google_domain": "google.com",
            "api_key": SERP_API_KEY
        }
        response = GoogleSearch(params)
        search = response.get_dict()["organic_results"]
        search = [[result["snippet"], result["link"]] if "snippet" in result.keys() else [] for result in search[:n+1 if len(search) >= n else len(search)]][1:]

    return search


ERPCLIENT = None

#@fuckit
def get_erp_api_result(method, *args, **kwargs):
    if consts.VIEWER:
        print(kwargs)
        print(method)
    global ERPCLIENT
    if not ERPCLIENT:
        from frappeclient import FrappeClient

        ERPCLIENT = FrappeClient(consts.URL_ERP, consts.USER_ERP, consts.PASSWORD_ERP, verify=False)    
    
    
    return getattr(ERPCLIENT, method)(*args, **kwargs)
    
    