# -*- coding: utf-8 -*-
from financial.calc_engine import CalcEngine
from data.rebuild import Rebuild
from PyFin.api import *
import pdb,time,datetime
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    rebuild = Rebuild('mysql+mysqlconnector://factor_edit:factor_edit_2019@db1.irongliang.com/vision?charset=utf8')
    # rebuild.rebuild_table('technical.price_volume','PriceVolume')
    # rebuild.rebuild_table('technical.momentum','Momentum')
    # rebuild.rebuild_table('technical.power_volume','PowerVolume')
    # rebuild.rebuild_table('technical.reversal','Reversal')
    # rebuild.rebuild_table('technical.sentiment','Sentiment')
    rebuild.rebuild_table('financial.volatility_value', 'VolatilityValue')
    
    calc_engine = CalcEngine('rl','mysql+mysqlconnector://factor_edit:factor_edit_2019@db1.irongliang.com/vision?charset=utf8')
    # print(calc_engine.local_run('2018-12-28'))

    # begin_date = '2017-08-26'
    begin_date = '2019-08-26'
    end_date = '2019-08-27'
    freq = '1b'
    rebalance_dates = makeSchedule(begin_date, end_date, freq, 'china.sse', BizDayConventions.Preceding)
    #rebalance_dates=[datetime.datetime(2019,8,26)]
    rebalance_dates.reverse()
    for date in rebalance_dates:
        start_time = time.time()
        calc_engine.local_run(date.strftime('%Y-%m-%d'))
        print(date, time.time()-start_time)





