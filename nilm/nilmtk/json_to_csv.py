from __future__ import print_function, division
from Utils.HttpRequest import HttpRequest as request
import csv

#Precisa de dados para testar
request.setUrl('1016', '/01/05/2020')
x = request.getTrainIA()

for dv in x.records:
    print(dv.idHardware)
    with open(dv.idHardware[:2]+dv.idHardware[15:]+'.csv', 'w') as arquivo_csv:
        colunas = ['power', 'date']
        escrever = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=';', lineterminator='\n')
        escrever.writeheader()

        for pbd in dv.powersByDate:
            escrever.writerow({'power': pbd.get_power(), 'date': pbd.get_date()})



