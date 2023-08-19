from flask import Blueprint, render_template, request, flash, redirect, url_for

views = Blueprint('views', __name__)

# Views
# Directory
# Dash Board
# Budget_dummmy
# Nutrition_dummy
# Data (from models)
# Budget (stored in auth)
# Nutrition ( and password protected)

# Directory
@views.route('/', methods=['Get', 'Post'])
def home():
    return  render_template("index.html")


# Dashboard
@views.route('/stocks', methods=['GET', 'POST'])
def dash():
    TIKKER = ['TSLA']  # Define TIKKER outside of the if block
    stock = None  # Initialize stock with None

    if request.method == 'POST':
        stock = request.form.get("TiKer")
        print(stock)

        if stock not in TIKKER:
            flash('At the moment the model is only trained for the following Tickers:', category='error')
        
        # redirect back to the same endpoint but as a GET request
        return redirect(url_for('views.dash'))

    return render_template("dash.html")

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