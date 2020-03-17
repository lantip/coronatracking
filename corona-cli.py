#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
__version__     =   "0.0.1"
__author__      =   "@lantip"
__date__        =   "2020/03/17"
__description__ =   "Corona CLI Indonesia"
"""
from bs4 import BeautifulSoup
import requests
from prettytable import PrettyTable
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import shutil
from itertools import count
import sys
import argparse
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getimage():
    r =  requests.get('https://infeksiemerging.kemkes.go.id/', verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    lists = soup.find_all('a')
    imej = None
    for lis in lists:
        if 'situasi-infeksi-emerging' in lis.get('href'):
            if len(lis.contents) > 0:
                try:
                    if lis.contents[0].get('src'):
                        imej = lis.contents[0].get('src')
                except:
                    pass
    return imej

def saveimage(imej):
    r = requests.get(imej,verify=False, stream=True)
    skrg = datetime.now()
    ext  = imej.split('.')[-1]
    with open('kemkesimage/'+str(skrg)+'.'+ext,'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    return 'kemkesimage/'+str(skrg)+'.'+ext

def parseimage(image):
    img_cv  = cv2.imread(image)
    #img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)   
    hasil = pytesseract.image_to_string(img_cv)
    #data =  pytesseract.image_to_data(Image.open(image))
    #print(data)
    try:
        hasil = hasil.split('\n')
    except:
        return []
    result = []
    for hs in hasil:
        if hs.strip() != '':
            result.append(hs)
    diperiksa = 0
    meninggal = 0
    positif = 0
    sembuh = 0
    negatif = 0
    proses = 0

    for idx,rs in enumerate(result):
        if idx > 0:
            if 'indonesia' in result[idx-1].lower():
                if 'jumlah' in rs.lower():
                     diperiksa = rs.split()[-1]
            if 'positif' in rs.lower():
                if 'meninggal' in rs.lower():
                    meninggal = rs.split()[-1]
                else:
                    positif = rs.split()[-1]
            if 'sembuh' in rs.lower():
                sembuh = rs.split()[-1]
            if 'negatif' in rs.lower():
                negatif = rs.split()[-1]
            if 'roses' in rs.lower():
                proses = rs.split()[-1]
            if 'prose ' in rs.lower():
                proses = rs.split()[-1]

    return [diperiksa,positif,sembuh,meninggal,negatif,proses]

def gettable(table):
    t = PrettyTable(['Diperiksa', 'Positif','Sembuh','Meninggal', 'Negatif', 'Proses'])
    t.add_row(table)
    return t

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('-o', '--output', type=str, default='spring', help="Output: 'table' atau 'csv'", required=True)
    args = parser.parse_args()

    output = args.output

    start = getimage()

    image = saveimage(start)

    parse = parseimage(image)

    if output == 'table':
        table = gettable(parse)
        print(table)

if __name__ == '__main__':
    main()