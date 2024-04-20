# def trade_day_producer():
#     from market_data.pipeline.trade_day.producer import TradeDayProducer
#
#     return TradeDayProducer
#
#
# def trade_day_processor():
#     from market_data.pipeline.trade_day.processor import TradeDayProcessor
#
#     return TradeDayProcessor
#
#
# def trade_day_storager():
#     from market_data.pipeline.trade_day.storager import TradeDayStorager
#
#     return TradeDayStorager


from market_data.pipeline.trade_day.bao_stock.producer import TradeDayProducer as BaoStockTradeDayProducer
from market_data.pipeline.trade_day.bao_stock.processor import TradeDayProcessor as BaoStockTradeDayProcessor
from market_data.pipeline.trade_day.bao_stock.storager import TradeDayStorager as BaoStockTradeDayStorager

BaoStockTradeDayProducer.set_component_name('BaoStockTradeDayProducer')
BaoStockTradeDayProcessor.set_component_name('BaoStockTradeDayProcessor')
BaoStockTradeDayStorager.set_component_name('BaoStockTradeDayStorager')

