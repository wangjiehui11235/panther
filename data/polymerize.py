# -*- coding: utf-8 -*-

import pdb
from .fech_data import MarketFactory, ExposureFactory, IndexMarketFactory, FetchEngine
#提取对应数据，并且进行预处理

#适配
class Adaptation(object):
    def __init__(self, name):
        self._name = name
        
    def market(self, data):
        raise NotImplementedError
        
    def risk_exposure(self, data):
        raise NotImplementedError
    
    @classmethod
    def create_adaptation(cls, name):
        if name == 'rl':
            return RLAdaptation(name)
        elif name == 'dx':
            return DXAdaptation(name)
        

class DXAdaptation(Adaptation):
    def __init__(self, name):
        super(DXAdaptation,self).__init__(name)
    
    def market(self, data):
        return data.rename(columns={'preClosePrice':'pre_close','openPrice':'open_price',
                                    'highestPrice':'highest_price','lowestPrice':'lowest_price',
                                    'closePrice':'close_price','turnoverVol':'turnover_vol',
                                    'turnoverValue':'turnover_value','accumAdjFactor':'factor',
                                    'vwap':'vwap','negMarketValue': 'neg_mkt_value',
                                    'marketValue': 'mkt_value','chgPct': 'chg_pct','isOpen': 'is_open',
                                    'PE': 'pe_ttm','PE1': 'pe','PB': 'pb'})
    
    def risk_exposure(self, data):
        return data

    def index_market(self, data):
        return data.rename(columns={'indexCode':'index_code', 'preCloseIndex':'pre_close_index',
                                    'openIndex':'open_index', 'highestIndex':'highest_index',
                                    'lowestIndex':'lowest_index', 'closeIndex':'close_index',
                                    'turnoverVol':'turnover_vol_index',
                                    'turnoverValue':'turnover_value_index',
                                    'chgPct':'chg_pct_index'})

    def calc_adaptation(self, data):
        return data

class RLAdaptation(Adaptation):
    def __init__(self, name):
        super(RLAdaptation,self).__init__(name)
        
    def market(self, data):
        return data.rename(columns={'symbol':'code','open':'open_price','close':'close_price',
                                   'high':'highest_price','low':'lowest_price','volume':'turnover_vol',
                                   'money':'turnover_value','change_pct':'chg_pct','tot_mkt_cap':'mkt_value',
                                   'factor':'factor'})
    def risk_exposure(self, data):
        return data.rename(columns={'symbol':'code'})

    def index_market(self, data):
        return data.rename(columns={'name':'name_index','pre_close':'pre_close_index','open':'open_index',
                                    'close':'close_index','high':'high_index','low':'low_index',
                                    'volume':'turnover_vol_index','money':'turnover_value_index',
                                    'change':'change_index','change_pct':'chg_pct_index'
                                    })

    #缺少vwap
    def calc_adaptation(self, data):
        data['vwap'] = data['turnover_value'] / data['turnover_vol']
        return data
    
    
class DBPolymerize(object):
    def __init__(self, name):
        self._name = name
        self._factory_sets = {
            'market': MarketFactory(FetchEngine.create_engine(name)),
            'exposure':ExposureFactory(FetchEngine.create_engine(name)),
            'index_market':IndexMarketFactory(FetchEngine.create_engine(name))
        }
        self._adaptation = Adaptation.create_adaptation(name)
     
    def fetch_data(self, begin_date, end_date, freq=None):
        market_data = self._factory_sets['market'].result(begin_date, end_date, freq)
        # exposure_data = self._factory_sets['exposure'].result(begin_date, end_date, freq)
        market_data = self._adaptation.market(market_data)
        # exposure_data = self._adaptation.risk_exposure(exposure_data)
        # total_data = market_data.merge(exposure_data, on=['code','trade_date'])
        total_data = market_data  # tmp
        return self._adaptation.calc_adaptation(total_data)

    def fetch_index_data(self, begin_date, end_date, freq=None):
        index_market_data = self._factory_sets['index_market'].result(begin_date, end_date, freq)
        index_market_data = self._adaptation.index_market(index_market_data)
        total_data = index_market_data
        return total_data
