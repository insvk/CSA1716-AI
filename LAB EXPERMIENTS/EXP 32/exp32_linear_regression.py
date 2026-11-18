import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Generate sample continuous data
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([2.3, 4.1, 6.2, 8.0, 10.1, 11.9, 14.1, 15.8, 18.2, 20.0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Implement Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Predictions: {predictions}")
print(f"Mean Squared Error: {mean_squared_error(y_test, predictions)}")