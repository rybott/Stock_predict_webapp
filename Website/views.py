from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image



from Code.processing import Stock_Graph

views = Blueprint('views', __name__)

# Views
# Directory
# Dash Board
# Budget_dummmy
# Nutrition_dummy
# Data (from models)
# Budget (stored in auth)
# Nutrition ( and password protected)



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

            # Graph
            plt.figure(figsize=(4, 1.5))
            Stock_Graph(stock, '5d')  # This function currently doesn't return anything
            img1 = io.BytesIO()
            plt.savefig(img1, format='jpeg')
            plt.close()  # Clear the current plot after saving
            img1.seek(0)
            with Image.open(img1) as im:
                buffered = io.BytesIO()
                im.save(buffered, format="JPEG", quality=20, optimize=True, progressive=True, exif=b'')
                buffered.seek(0)
                session['plot_url1'] = base64.b64encode(buffered.getvalue()).decode('utf8')

            session['output_string1'] = Stock_Graph(stock, '10d')

        return redirect(url_for('views.dash'))

    # Fetch the values from session with default values to avoid KeyError
    TICKER = session.get('TIK', 'Default Ticker')
    output_string = session.get('output_string1', '')
    plot_url = session.get('plot_url1', None)

    return render_template("dash.html", TICKER=TICKER, output_string=output_string, plot_url=plot_url)


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