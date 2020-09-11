from __future__ import print_function, division
import os
import json
import pickle
import pandas as pd
import simplejson as s_json
from copy import deepcopy as copy
from nilmtk.disaggregate import fhmm_exact
from Utils.PowerRecord import PowerRecord as pr
from Utils.HttpRequest import HttpRequest as rq
from Utils.DisaggregatePowerRecord import DisaggregatePowerRecord as dpr


store_name = './store/table/'
power = 'power'
id_server = 'id_server'


def save_table(house, day_last_get, hour_last_get):
    rq.setUrl(house, day_last_get, hour_last_get)
    x = rq.getTrainAI()
    if x is None:
        return None
    else:
        db = pd.HDFStore(store_name+house+'.h5')
        type = 'main_'
        for dv in x.records:
            dv_id = dv.idHardware
            data, index = dv.power_time_id()

            df = pd.DataFrame(data, index=index, columns=['power', 'id_server'])
            db.put(house + '/' + type + dv_id + '/data', df, format='table', append=True, data_columns=True)
            type = 'meter_'
        db.close()
        return x.meters()


def load_table(house):
    try:
        with pd.HDFStore(store_name+house+'.h5', mode='r') as hdf:
            devices_list = []
            for key in hdf.keys():
                f = pd.read_hdf(store_name+house+'.h5', key=key)
                consumos = []
                key = key.split("/")

                index_list = f.index.tolist()
                power_list = f[power].values.tolist()
                id_list = f[id_server].values.tolist()
                id_house = key[1]
                id_meter = key[2].split('_')[1]

                for i, index in enumerate(index_list):
                    consumos.append({'potencia': power_list[i], 'dataRegistro': index, 'idConsumo': id_list[i]})
                devices_list.append({'idHardware': id_meter, 'questao': '', 'resposta': '', 'consumos': consumos})

            return pr({'registros': devices_list, 'dataFinal': 'data_base'})
    except ValueError as err:
        print(err)
        return None


def save_model(house, fhmm):
    with open("./store/model/model_" + house + ".pkl", "wb") as file:
        pickle.dump(fhmm.model, file)
        file.close()
    with open("./store/model/individual_" + house + ".pkl", "wb") as file:
        pickle.dump(fhmm.individual, file)
        file.close()


def load_model(house):
    fhmm = fhmm_exact.FHMM()
    try:
        with open("./store/model/model_" + house + ".pkl", "rb") as file:
            fhmm.model = pickle.load(file)
            file.close()
        with open("./store/model/individual_" + house + ".pkl", "rb") as file:
            fhmm.individual = pickle.load(file)
            file.close()
        return fhmm
    except ValueError as err:
        print(err)
        return None


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



