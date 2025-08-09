import requests
from bs4 import BeautifulSoup
import json
import re
import xml.etree.ElementTree as ET
import os
from urllib.parse import unquote
from urllib.parse import urlparse, urlunparse
from datetime import datetime
import unicodedata
import urllib3

# Disable the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_proxies(country_code):
    url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country={country_code}&ssl=all&anonymity=elite"
    response = requests.get(url)
    if response.status_code == 200:
        proxy_list = response.text.splitlines()
        return [f"socks4://{proxy}" for proxy in proxy_list]
    else:
        print(f"Failed to fetch proxies for {country_code}. Status code: {response.status_code}")
        return []

def fetch_channel_list(proxy, retries=3):
    url = "https://tubitv.com/live"
    for attempt in range(retries):
        try:
            if proxy:
                response = requests.get(url, proxies={"http": proxy, "https": proxy}, verify=False, timeout=20)
            else:
                response = requests.get(url, verify=False, timeout=20)
            response.encoding = 'utf-8'
            if response.status_code != 200:
                print(f"Failed to fetch data from {url} using proxy {proxy}. Status code: {response.status_code}")
