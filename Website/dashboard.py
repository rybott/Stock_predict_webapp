from flask import Blueprint, render_template, request, flash

dashboard = Blueprint('dashboard', __name__)\

@dashboard.route('/dashboard', methods=['Get', 'Post'])
def home():
    if request.method == 'POST':
        TIK = request.form.get(TIK)
        TIKKER = ['TSLA']

    if TIK != TIKKER:
        flash(f'At the moment the model is on trained for the following Tickers: {TIKKER}', category='error')
    return render_template("dash.html")