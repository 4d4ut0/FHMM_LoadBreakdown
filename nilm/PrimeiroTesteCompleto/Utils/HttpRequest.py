import urllib.request
import requests
import json
import simplejson as sjson
from Utils.PowerRecord import PowerRecord as pr
from Utils.DisaggregatePowerRecord import DisaggregatePowerRecord as dpr

def_url = ['http://nexsolar.sytes.net/ceb/api/desagregacao/', 'http://nexsolar.sytes.net/ceb/api/desagregacao/main/', 'http://nexsolar.sytes.net/ceb/api/desagregacao/']


def escrever_txt(lista):
    with open('meu_arquivo.txt', 'w', encoding='utf-8') as f:
        f.write(lista)


class HttpRequest(object):
    URL = {
        'getTrainAI': 'http://nexsolar.sytes.net/ceb/api/desagregacao/',
        'getDisaggregate': 'http://nexsolar.sytes.net/ceb/api/desagregacao/main/',
        'postDisaggregate': 'http://nexsolar.sytes.net/ceb/api/desagregacao/'
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    date = "None"

    @classmethod
    def setUrl(cls, idAddress, lastTimeStamp):
        cls.URL['getTrainAI'] = def_url[0] + idAddress + lastTimeStamp
        cls.URL['getDisaggregate'] = def_url[1] + idAddress + lastTimeStamp
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
    def postDisaggregate(cls, obj):
        jsonObj = sjson.loads(cls.renameJson(dpr(obj).toJSON()))
        jsonObj = jsonObj['registros']


        # arrumando um bg não encontrado
        if 'registros' in jsonObj:
            if 'chunks' in jsonObj['registros'][0]:
                del jsonObj['registros'][0]['chunks']
                for i in jsonObj['registros']:
                    if 'chunks' in i:
                        del i['chunks']

        with open('log_send_server.json', 'w') as f:
            json.dump(jsonObj, f)

        r = requests.post(cls.URL['postDisaggregate'], data=json.dumps(jsonObj), headers=cls.headers)
        print(r.text, r)
        return r.text

    @classmethod
    def renameJson(cls, obj):
        obj = obj.replace('records', 'registros')
        obj = obj.replace('lastTimeStamp', 'dataFinal')
        obj = obj.replace('query', 'questao')
        obj = obj.replace('answer', 'resposta')
        obj = obj.replace('power', 'potencia')
        obj = obj.replace('powerByDate', 'consumos')
        obj = obj.replace('potenciasByDate', 'consumos')
        obj = obj.replace('date', 'dataRegistro')
        return obj.replace('lastTimeStamp', 'dataFinal')



