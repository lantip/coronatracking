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
    if not imej:
        for lis in lists:
            if 'download' in lis.get('href'):
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
    #img_cv  = cv2.imread(image)
    #img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)   
    #hasil = pytesseract.image_to_string(img_cv)
    hasil =  pytesseract.image_to_string(Image.open(image))
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
    print(result)
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
    t = PrettyTable(['Hari ke', 'Penambahan Kasus Hari ini', 'Total Kasus Positif','Sembuh','Meninggal', 'Dalam Perawatan'])
    t.add_row(table)
    return t

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('-o', '--output', type=str, default='spring', help="Output: 'table' atau 'csv'", required=True)
    args = parser.parse_args()

    output = args.output

    #start = getimage()

    #image = saveimage(start)

    #parse = parseimage(image)
    r = requests.get('https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/ArcGIS/rest/services/Statistik_Perkembangan_COVID19_Indonesia/FeatureServer/0/query?where=FID%3E0&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token=', verify=False)
    data = r.json()
    features = data['features']
    awal = datetime(2020,3,1)
    skrg = datetime.now()
    sisa = skrg - awal
    tabel = []
    for tbl in features:
        attrib = tbl['attributes']
        if attrib['Hari_ke'] == sisa.days:
            if attrib['Jumlah_Kasus_Baru_per_Hari']:
                tabel = [ attrib['Hari_ke'], attrib['Jumlah_Kasus_Baru_per_Hari'], attrib['Jumlah_Kasus_Kumulatif'], attrib['Jumlah_Pasien_Sembuh'], attrib['Jumlah_Pasien_Meninggal'], attrib['Jumlah_pasien_dalam_perawatan'] ]
    if len(tabel) < 1:
        print('Data hari ini belum diumumkan. \nData hari kemarin adalah')
        for tbl in features:
            attrib = tbl['attributes']
            if attrib['Hari_ke'] == (int(sisa.days) - 1):
                if attrib['Jumlah_Kasus_Baru_per_Hari']:
                    tabel = [ attrib['Hari_ke'], attrib['Jumlah_Kasus_Baru_per_Hari'], attrib['Jumlah_Kasus_Kumulatif'], attrib['Jumlah_Pasien_Sembuh'], attrib['Jumlah_Pasien_Meninggal'], attrib['Jumlah_pasien_dalam_perawatan'] ]
    if output == 'table':
        result = gettable(tabel)
        print(result)

if __name__ == '__main__':
    main()