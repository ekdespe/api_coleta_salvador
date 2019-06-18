# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import config as c
import pymongo

def init_db():
    
    client = pymongo.MongoClient(c.CONFIG['url_database'])
    db = client[c.CONFIG['name_database']]
    col = db[c.CONFIG['name_collection']]
    
    page = requests.get(c.CONFIG['url_request_init'])
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find("script",{"type":"text/javascript"})
    result = result.get_text()
    pattern = re.compile(r'locais = \[.*?]', re.MULTILINE | re.DOTALL)
    match = pattern.search(result)
    if match:
        locais = [(match.group(0))]
        locais = locais[0].replace("locais = ","")
        locais = locais.replace("titulo:","\"titulo\":")
        locais = locais.replace("latitude:","\"latitude\":")
        locais = locais.replace("longitude:","\"longitude\":")
        locais = locais.replace("end:","\"end\":")
        locais = locais.replace("tipo:","\"tipo\":")
        locais = locais.replace("tipo_descricao:","\"tipo_descricao\":")
        locais = locais.replace("ponto_referencia:","\"ponto_referencia\":")
        locais = json.loads(locais)
        for key in locais:
            if key.get('latitude'):
                latitude = float(key.pop('latitude'))
            else:
                latitude = 0
                key.pop('latitude')
            if key.get('longitude'):
                longitude= float(key.pop('longitude'))
            else:
                longitude = 0
                key.pop('longitude')

            key.update({"localizacao":{"type":"Point","coordinates":[longitude,latitude]}})
            
        col.insert_many(locais)
if __name__ == '__main__':
    init_db()

