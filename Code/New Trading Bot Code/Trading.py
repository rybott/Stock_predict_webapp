import asyncio
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, CryptoTrade
from typing import List
from polygon import RESTClient
import pandas as pd
import ast

import threading
import time

from TrendAnalysis import TradeBuffer

class Broker_Information:
    


