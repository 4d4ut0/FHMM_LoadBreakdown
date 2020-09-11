import urllib.request
import requests
import json
import simplejson as sjson
from Utils.PowerRecord import PowerRecord as pr
from Utils.Consumos import Consumos as cs

def_url = ['http://nexsolar.sytes.net/chesp/api/desagregacao/', 'http://nexsolar.sytes.net/chesp/api/desagregacao/main/', 'http://nexsolar.sytes.net/chesp/api/desagregacao/fisicos', 'http://nexsolar.sytes.net/chesp/api/desagregacao/virtuais']


def escrever_txt(lista):
    with open('meu_arquivo.txt', 'w', encoding='utf-8') as f:
        f.write(lista)

class HttpRequest(object):
    URL = {
        'getTrainAI': 'http://nexsolar.sytes.net/chesp/api/desagregacao/',
        'getDisaggregate': 'http://nexsolar.sytes.net/chesp/api/desagregacao/main/',
        'postDisaggregateF': 'http://nexsolar.sytes.net/chesp/api/desagregacao/fisicos',
        'postDisaggregateV': 'http://nexsolar.sytes.net/chesp/api/desagregacao/virtuais',

    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    date = "None"

    @classmethod
    def setUrl(cls, idAddress, lastTimeStamp, h):
        cls.URL['getTrainAI'] = def_url[0] + idAddress + lastTimeStamp
        cls.URL['getDisaggregate'] = def_url[1] + idAddress + lastTimeStamp + h
        cls.date = idAddress + lastTimeStamp
        cls.date.replace('/', '_')

    @classmethod
    def getTrainAI(cls):
        try:
            with urllib.request.urlopen(cls.URL['getTrainAI']) as url:
                data = json.loads(url.read().decode())
                return pr(data)
        except Exception as e:
            return None

    @classmethod
    def local_getTrainAI(cls, file_name):
        try:
            with open(file_name, 'r') as url:
                data = json.load(url)
                return pr(data)
        except Exception as e:
            return None

    @classmethod
    def getDisaggregate(cls):
        try:
            with urllib.request.urlopen(cls.URL['getDisaggregate']) as url:
                data = json.loads(url.read().decode())
                return pr(data)
        except Exception as e:
            return None

    @classmethod
    def postDisaggregateF(cls, obj):
        jsonObj = sjson.loads(cls.renameJson(obj.toJSON()))

        with open('log_send_server_fisical.json', 'w') as f:
            json.dump(jsonObj, f)

        r = requests.post(cls.URL['postDisaggregateF'], data=json.dumps(jsonObj), headers=cls.headers)
        print(r.text, r)
        return r.text

    @classmethod
    def postDisaggregateV(cls, obj):
        jsonObj = sjson.loads(cls.renameJson(obj.toJSON()))
        #jsonObj = jsonObj['consumos']

        # arrumando um bg não encontrado
        try:
            if 'consumos' in jsonObj:
                if 'chunks' in jsonObj['consumos'][0]:
                    del jsonObj['consumos'][0]['chunks']
                    for i in jsonObj['consumos']:
                        if 'chunks' in i:
                            del i['chunks']
        except IndexError:
            print('elemento vazio')

        with open('log_send_server.json', 'w') as f:
            json.dump(jsonObj, f)

        with open('log_send_serve_virtual.json', 'w') as f:
            json.dump(jsonObj, f)

        r = requests.post(cls.URL['postDisaggregateF'], data=json.dumps(jsonObj), headers=cls.headers)
        print(r.text, r)
        return r.text

    @classmethod
    def renameJson(cls, obj):
        obj = obj.replace('records', 'consumos')
        obj = obj.replace('lastTimeStamp', 'dataFinal')
        obj = obj.replace('query', 'questao')
        obj = obj.replace('answer', 'resposta')
        obj = obj.replace('power', 'potencia')
        obj = obj.replace('powerByDate', 'consumos')
        obj = obj.replace('potenciasByDate', 'consumos')
        obj = obj.replace('date', 'dataRegistro')
        return obj.replace('lastTimeStamp', 'dataFinal')

    @classmethod
    def send_fisicos(cls, disaggregate):
        envio = cs()
        for dv in disaggregate.records:
            envio.add_fisicos(dv.make2disagregate())
        cls.postDisaggregateF(envio)

    @classmethod
    def send_virtuais(cls, disaggregate):
        cls.postDisaggregateV(disaggregate)
