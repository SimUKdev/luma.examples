#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Michael Svanström, Richard Hull and contributors
# See LICENSE.rst for details.
## Updated version by SimUK, April 2021. Based on bitstamp_ticker.py example
# PYTHON_ARGCOMPLETE_OK

"""
Displays the Bitcoin price at Bitstamp
Example:
BTC/USD 
$50400.00
24h Hi $51000.00
24h Lo $48000.00
"""

import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("The requests library was not found. Run 'sudo -H pip install requests' to install it.")
    sys.exit()

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont



def fetch_price(crypto_currency, fiat_currency):
    bitstamp_api = "https://www.bitstamp.net/api/v2/ticker/" + crypto_currency.lower() + fiat_currency.lower()
    try:
        r = requests.get(bitstamp_api)
        return r.json()
    except:
        print("Error fetching from Bitstamp API")


def get_price_text(crypto_currency, fiat_currency):
    data = fetch_price(crypto_currency, fiat_currency)
    return [
        '{}/{}'.format(crypto_currency, fiat_currency, data['last']),
        '{}'.format(data['last']),
        '24h Hi {}'.format(data['high']),
        '24h Lo {}'.format(data['low'])
    ]



def show_price(device):
    # use custom font
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 20)
    fontcryptoname = ImageFont.truetype(font_path, 18)
    fontbigger = ImageFont.truetype(font_path, 34)
    fontsmall = ImageFont.truetype(font_path, 16)


    with canvas(device) as draw:
        # BTC USD
        rows = get_price_text("BTC", "USD")
        draw.rectangle((0, 0, device.width, 15), outline="#0c0c0c", fill="#0c0c0c")
        draw.rectangle((0, 16, device.width, device.height), outline="#050505", fill="#050505")
        draw.text((4, 0), rows[0], font=fontcryptoname, fill="#828200")
        draw.text((4, 14), rows[1], font=fontbigger, fill="#e0e0e0")

        if device.height >= 64:
            draw.text((4, 48), rows[2], font=fontsmall, fill="#d9d9d9")
            draw.text((4, 62), rows[3], font=fontsmall, fill="#d9d9d9")



def main():
    while True:
        show_price(device)
        time.sleep(60)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
