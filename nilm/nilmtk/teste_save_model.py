import matplotlib.pyplot as pl
import Utils.save_manager as sm
from nilmtk.disaggregate import fhmm_exact
from Utils.HttpRequest import HttpRequest as rq

house = '1016'

#sm.save_table('1016', '/29/5/2020', '/00/00')

#store_data = sm.load_table(house)
#fhmm = fhmm_exact.FHMM()
#fhmm.nexTrain(store_data.meters())

#sm.save_model(house, fhmm)
fhmm = sm.load_model(house)

rq.setUrl('1016', '/15/6/2020', '/00/00')
x = rq.getDisaggregate()
main = x.main()
disaggregate = fhmm.nexDisaggregate(main)
for dv in disaggregate.records:
    dv.idHardware = 'ia_'+dv.idHardware
    dv.get_energy2()

'''
for dv in disaggregate.records:
    power, time = dv.power_time()
    pl.plot(time, power, 'r')
    pl.gcf().autofmt_xdate()
    pl.title(dv.idHardware)
    pl.show()
'''
rq.send_virtuais(disaggregate)