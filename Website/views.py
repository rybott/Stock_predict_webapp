from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import os
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import nest_asyncio
from transformers import pipeline
load_dotenv()

from Code.processing import *
from Code.tweet import Get_TW

since1 = datetime.today() - timedelta(days=1)
since = since1.date()
views = Blueprint('views', __name__)
nest_asyncio.apply()

# Views
# Directory
# Dash Board
# Budget_dummmy
# Nutrition_dummy
# Data (from models)
# Budget (stored in auth)
# Nutrition ( and password protected)

@views.route('stock_data/<string:TICK>/<string:period>')
def get_data(TICK, period):
    TIKKER = ['TSLA', 'NOC', 'PG', 'TSM', 'VZ', 'BX', 'BA', 'AMD', 'CRM', 'COST', 'AMZN', 'GOOG', 'DIS', 'KO', 'META', 'INTC', 'MSFT']

    if TICK not in TIKKER:
        # handle the case where the session variable is not set
        return jsonify(error="Ticker not set in session"), 400
    data = Stock_Graph(TICK, period)  
    return jsonify(data)


# Dashboard
@views.route('/', methods=['GET', 'POST'])
def dash():
    TIKKER = ['TSLA', 'NOC', 'PG', 'TSM', 'VZ', 'BX', 'BA', 'AMD', 'CRM', 'COST', 'AMZN', 'GOOG', 'DIS', 'KO', 'META', 'INTC', 'MSFT']
    
    if request.method == 'POST':
        stock = request.form.get("TiKer")
        print(stock)

        if stock not in TIKKER:
            flash('This is not a known Ticker. Please refresh the screen to try another of these options: ', category='error')
        else:
            session['TIK'] = stock
            # Current Price
            session['current_price'] = Stock_Price(session['TIK'])
            # News Articles
            n = 6 
            session['News'] = News(session['TIK'],n)
            # Tweets
            Senti = Get_TW(stock,since)
            session['TW_Sentiment'] = Senti[0]
            session['TW_Score'] = Senti[1]

        return redirect(url_for('views.dash'))
    return render_template("dash.html", TICKER=session.get('TIK', 'N/A'), 
                       PRICE=session.get('current_price', '0.00'),
                       NEWS=session.get('News', []), SENTI=session.get('TW_Sentiment', 'N/A'),
                       CONFI=session.get('TW_Score', 'N/A'))

# Directory (Make sure to turn it into main page with '/' before makie other pages)








@views.route('/directory', methods=['Get', 'Post'])
def home():
    return  render_template("index.html")

# Data
@views.route('/data', methods=['Get', 'Post'])
def data():
    return "<h1>Login IN <h1>"

# Budget_dummy
@views.route('/budget_', methods=['Get', 'Post'])
def budget0():
    return "<h1>Comming Soon <h1>"

# Nutrition_dummy
@views.route('/nutrition_', methods=['Get', 'Post'])
def nutrition0():
    return "<h1>Comming Soon <h1>"