import time
import pandas as pd

Current_Time = time.strftime("%Y-%h-%d %H:%M:%S",time.localtime())
Time_Formatted = pd.to_datetime(Current_Time)
