from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import asyncio
'''
from twscrape import API, gather
from twscrape.logger import set_log_level
import nest_asyncio
from transformers import pipeline
'''
load_dotenv()

from Code.processing import *

since1 = datetime.today() - timedelta(days=1)
since = since1.date()
views = Blueprint('views', __name__)


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
            n = 10
            session['News'] = News(session['TIK'],n)
            # Tweets
            # NOT AVALIABLE 
            
            # Machine Learning Models
            ml = ML(session['TIK'])
            session ['Direction'] = "Increase" if ml[0] > 0 else "Decrease"
            session ['Score'] = abs(ml[1])

            # Technical Analysis
            session['analysis'] = request.form.get("Analysis")
            print(request.form.get("Analysis"))

            if session['analysis'] == 'true':
                session['High52'] = 'None'
                session['low52'] = 'None'
                session['Mid52'] = 'None'
                session['DilutedEPS'] = 'None'
                session['QuarterlyRevGrowthYOY'] = 'None'
                session['AnalystTargetPrice'] = 'None'
                session['netIncome'] = 'None'
                session['Gross_Margin'] = 'None'
                session['Current'] = 'None'
                session['Quick'] = 'None'
                session['Debt_Equity'] = 'None'
                session['Debt_Ratio'] = 'None'
                session['ROE'] = 'None'
                session['ROA'] = 'None'
            else:
                get = request.form.get("TiKer")
                RA = ratio_analysis(stock)
                session['High52'] = RA['High52']
                session['low52'] = RA['low52']
                session['Mid52'] = RA['Mid52']
                session['DilutedEPS'] = RA['DilutedEPS']
                session['QuarterlyRevGrowthYOY'] = RA['QuarterlyRevGrowthYOY']
                session['AnalystTargetPrice'] = RA['AnalystTargetPrice']
                session['netIncome'] = RA['netIncome']
                session['Gross_Margin'] = round(RA["Gross_Margin"]*100,2)
                session['Current'] = round(RA['Current'],3) 
                session['Quick'] = round(RA['Quick'],3)
                session['Debt_Equity'] = round(RA['Debt_Equity'],3) 
                session['Debt_Ratio'] = round(RA['Debt_Ratio'],3)
                session['ROE'] = round(float(RA['netIncome']) / float(RA['totalShareholderEquity']),3)
                session['ROA'] = round(float(RA['ebit']) / float(RA['totalAssets']),3)

            '''
            High52 
            low52
            DilutedEPS
            QuarterlyRevGrowthYOY
            AnalystTargetPrice
            netIncome
            Gross_Margin
            Current
            Quick
            Debt_Equity
            Debt_Ratio
            '''

        return redirect(url_for('views.dash'))
    return render_template("dash.html", 
                           TICKER=session.get('TIK', 'N/A'), 
                            PRICE=session.get('current_price', '0.00'),
                            NEWS=session.get('News', []), SENTI='N/A',
                            CONFI='0.00',
                            High52= session.get('High52'),
                            low52= session.get('low52'),
                            DilutedEPS= session.get('DilutedEPS'),
                            QuarterlyRevGrowthYOY= session.get('QuarterlyRevGrowthYOY'),
                            AnalystTargetPrice= session.get('AnalystTargetPrice'),
                            ebit= session.get('ebit'),
                            netIncome= session.get('netIncome'),
                            Gross_Margin= session.get('Gross_Margin'),
                            ROE = session.get('ROE'),
                            ROA = session.get('ROA'),
                            Current= session.get('Current'),
                            Quick= session.get('Quick'),
                            Debt_Equity= session.get('Debt_Equity'),
                            Debt_Ratio= session.get('Debt_Ratio'),
                            Direction= session.get('Direction'),
                            Score = session.get('Score'))

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