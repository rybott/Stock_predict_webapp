import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np
import pickle

# Data Processing
data = pd.read_excel('TrainingSP500Data.xlsx')
X = data.drop(['Predict', 'Close', 'date'], axis=1)
y = data['Predict']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model Training
random_forest_model = RandomForestRegressor(n_estimators=1000, random_state=42)
random_forest_model.fit(X_train, y_train)

# Testing and Reporting
y_pred = random_forest_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)
print("Mean Absolute Error:", mae)

perfect_predictions = np.linspace(min(y_test), max(y_test), 100)
plt.plot(perfect_predictions, perfect_predictions, 'r', label='Perfect Predictions')
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values")
plt.legend()
plt.show()

# save model
filename = 'SPModel2'
rf = random_forest_model

with open('StockRandomForrestModel3', 'wb') as f:
    pickle.dump(rf, f)