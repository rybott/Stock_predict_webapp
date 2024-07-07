import pandas_ta as ta
import pandas as pd


class Global_Var():
    def __init__(self):
        pass

class Stock_Analysis():
    def __init__(self,data,con):
        self.StockFlag = False
        self.df = pd.DataFrame.from_dict(data, orient='index')

    def swoosh():
        One = self.df['4. close'].iloc(0)
        Two = self.df['4. close'].iloc(1)
        Three = self.df['4. close'].iloc(2)
        Four = self.df['4. close'].iloc(3)

        if Two > Three and Four > Three and One > max(Two, Three, Four):
            return True
        else:
            return False

    def rsi():  
        rsi = ta.rsi(close=self.df['4. close'])

    def ema_min():

        # EMA's
        self.df['EMA8'] = ta.ema(close=self.df['4. close'],length=8)
        self.df['EMA20'] = ta.ema(close=self.df['4. close'],length=20)

        # Local Mins
        self.df['Local_Min'] = self.df['4. close'][(self.df['4. close'].shift(1) > self.df['4. close']) & 
                                                    (self.df['4. close'].shift(-1) > self.df['4. close'])]

        # Find all the Local Minimums
        local_mins = self.df[['Local_Min','EMA8']].dropna()
        if len(local_mins) < 2:
            return False
        
        # Check if the last two local minimums are increasing
        Min_Test = local_mins['Local_Min'].iloc[0] > local_mins['Local_Min'].iloc[1]
        if Min_Test == False:
            return False
        else:
            if local_mins['Local_Min'].iloc[-2] < local_mins['EMA8'].iloc[-2] and local_mins['Local_Min'].iloc[-1] < local_mins['EMA8'].iloc[-1]: 
                return False
            elif self.df['4. close'].tail(5).min() < self.df['EMA8'].iloc(-5):
                return False
            else:
                return True


    def analysis():

        if not self.swoosh():
            self.TradeStat = False
            return self.TradeStat

        if not self.ema_min():
            self.TradeStat = False
            return self.TradeStat

        self.TradeStat = True
        return self.TradeStat
