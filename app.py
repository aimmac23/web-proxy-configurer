""" WebProxyConfigurer App """

import csv
import io
from functools import reduce

from flask import Flask, request

import requests


app = Flask(__name__)


@app.route('/status')
def status():
    """ Status check for Kubernetes"""
    return 'OK'


def get_proxies(country=None, timeout=500):
    """
    Scrape proxies from the internet and return them in a list
    :param country:
    :param timeout:
    :return:
    """
    country_fragment = f"&country={country}" if country else ""

    url = f"https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=text&timeout={timeout}&protocol=socks5{country_fragment}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses

    # Decode bytes to text using the detected/declared encoding
    text = response.content.decode(response.encoding or "utf-8")

    # Use StringIO so csv can read from the in-memory string
    buffer = io.StringIO(text)

    reader = csv.reader(buffer)
    return list(reader)

@app.route('/proxies', methods=['get'])
def proxies():
    country = request.args.get('country', None)
    timeout = request.args.get('timeout', 500)
    count = request.args.get('count', 3, type=int)
    whitelist = request.args.getlist("whitelist")

    whitelist_expr = reduce(
        lambda a, b: a + " || " + b,
        map(lambda h: f"shExpMatch(host, '{h}')", whitelist)
    ) if whitelist else None

    proxy_list = get_proxies(country=country, timeout=timeout)

    proxy_expr = "'" + reduce(
        lambda a, b: a + "; " + b,
        map(lambda p: f"SOCKS5 {p[0]}", proxy_list[:count])
    ) + "'"

    if whitelist_expr:
        return "function FindProxyForURL(url, host) { if ( " + whitelist_expr + " ) { return " + proxy_expr +" ; } return 'DIRECT'; }"
    else:
        return "function FindProxyForURL(url, host) { return " + proxy_expr +" ; }"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
