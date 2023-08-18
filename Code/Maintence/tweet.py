import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import nest_asyncio



async def add_user(usr, pass1, eml, pass2):
    nest_asyncio.apply()
    api = API()
    await api.pool.add_account(usr, pass1, eml, pass2)
    await api.pool.login_all()