import pandas_ta as ta
import pandas as pd


class Global_Var():
    def __init__(self):
        pass

class Stock_Analysis():
    def __init__(self,data,con):
        self.StockFlag = False
        self.df = pd.DataFrame.from_dict(data, orient='index')

    def rsi():  
        rsi = ta.rsi(close=self.df['4. close'])

    def bollingerbands():
        pass

    def other():
        pass

    def analysis():

        if not self.rsi():
            self.TradeStat = False
            return self.TradeStat

        if not self.calculate_rsi():
            self.TradeStat = False
            return self.TradeStat

        if not self.calculate_moving_average():
            self.TradeStat = False
            return self.TradeStat

        self.TradeStat = True
        return self.TradeStat
