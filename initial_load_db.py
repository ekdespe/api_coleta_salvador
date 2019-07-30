# -*- coding: UTF-8 -*-
"""Webcrawler do site que fornece os pontos de coletiva na cidade de Salvador-BA.


O presente sofware utiliza a biblioteca BeautifulSoup e expressões regulares para extrair todos os pontos de coleta listados no site http://www.coletaseletiva.salvador.ba.gov.br/   estaticamente, parsear os dados para json e  inserir na instância mongodb desejada.Vale ressaltar que a ferramenta é não oficial.

Todas as dependências seguem listadas no arquivo requirements.txt
Todas as ações são gravadas no log.txt localizado na pasta /logs
Os arquivos de testes podem ser consultados na pasta /tests

"""
__author__ = "Erik Ferreira da Silva"
__copyright__ = "Copyleft 2019, by ekdespe"
__credits__ = "Todos desenvolvedores de software livre :)"
__license__ = "GNU General Public License"
__version__ = "1.0.0"
__maintainer__ = "Erik Ferreira da Silva"
__email__ = "ekdespe@gmail.com"
__status__ = "Prototype"
__date__ = "30 Julho 2019"


import requests
from logs import log as lg
from bs4 import BeautifulSoup
import json
import re
import pymongo
import os
import datetime
import settings
def extract_payload_from_website():
    """Extrator e parser da página web.

    Basicamente um get é realizado na url em questão através do beatifulSoup , e a expressão regular percorre o resultado buscando especificamente pela expressão  'var local =' que é a variável que guarda todos os locais na variável javascript da página contida na tag script.Atenção especial para a sanitização dos dados pois existem pontos de geolocalização que precisam ser adequados ao formato requerido pelo mongodb.
    """
    
    lg.lg.info("**Running script** in {}".format(datetime.datetime.now()))       
    
    try:
        page = requests.get(os.getenv('url_request_init'))
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
    except Exception as error:
        lg.lg.error("Error! Problem to extract content from server")
        lg.lg.error(error)
    else:
        lg.lg.info("Sucess! To  to extract content from server")
        insert_payload_in_db(locais)
    
    
    
    
    

def insert_payload_in_db(payload):
    """Insert dos locais na instância mongodb.
    Os dados são recebidos e a inserção é feita.Os dados da instância devem ser configuradas no arquivo .env que abriga as variáveis de ambiente.
    """
    try:
    
        client = pymongo.MongoClient(os.getenv('url_database'))
        db = client[os.getenv('name_database')]
        col = db[os.getenv('name_collection')]
        col.insert_many(payload)
    except Exception as error:
        lg.lg.error('Error! Failed to manipulate database conection')
        lg.lg.error(error)
    else:
        lg.lg.info('Success! Insert data into database')
        lg.lg.info("**End of  script** in {}".format(datetime.datetime.now()))            



if __name__ == '__main__':
    extract_payload_from_website()
