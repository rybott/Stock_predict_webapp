import requests
import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import time

from SQL.Querys import DBconn

Query = DBconn()
Create_Options = Query.CreateOptionTbl
Create_Stock = Query.CreateStockTbl

con = ddb.connect('TestingAlphaOptions.duckdb')

