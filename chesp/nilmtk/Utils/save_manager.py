import json
import os
import simplejson as s_json
from copy import deepcopy as copy
from Utils.DisaggregatePowerRecord import DisaggregatePowerRecord as dpr


def save_device(house, device, f_time, l_time, obj):
    file_name = f_time + '_' + l_time + '.json'
    file_path = 'input_train/' + house + '/' + device + '/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    json_obj = make_json_obj(obj)

    with open(file_path + file_name, 'w') as f:
        json.dump(json_obj, f)


def generate_records2save(power_record):
    records2save = []
    # retirar demais dv do record
    for dv in power_record.meters():
        copy_power_record = copy(power_record)
        for i, cdv in enumerate(power_record.records):
            if cdv.idHardware != dv.idHardware and i != 0:
                del copy_power_record.records[i]
        records2save.append(copy_power_record)
    return records2save


def rename_json(obj):
    obj = obj.replace('records', 'registros')
    obj = obj.replace('lastTimeStamp', 'dataFinal')
    obj = obj.replace('query', 'questao')
    obj = obj.replace('answer', 'resposta')
    obj = obj.replace('power', 'potencia')
    obj = obj.replace('powerByDate', 'consumos')
    obj = obj.replace('potenciasByDate', 'consumos')
    obj = obj.replace('date', 'dataRegistro')
    return obj.replace('lastTimeStamp', 'dataFinal')


def make_json_obj(obj):
    json_obj = s_json.loads(rename_json(dpr(obj).toJSON()))
    json_obj = json_obj['registros']

    # arrumando um bg não encontrado
    if 'registros' in json_obj:
        if 'chunks' in json_obj['registros'][0]:
            del json_obj['registros'][0]['chunks']
            for i in json_obj['registros']:
                if 'chunks' in i:
                    del i['chunks']

    return json_obj



