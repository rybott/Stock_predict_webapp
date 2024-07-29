import requests
import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import time
import datetime

load_dotenv()
api_key = os.getenv("Alpha_API")
con = ddb.connect('datadump.duckdb')

