import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Generate continuous sample data
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([2.3, 4.1, 6.2, 8.0, 10.1, 11.9, 14.1, 15.8, 18.2, 20.0])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f"Slope (coefficient): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"Predictions: {np.round(predictions, 2)}")
print(f"Actual values: {y_test}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, predictions):.4f}")
print(f"Mean Squared Error: {mean_squared_error(y_test, predictions):.4f}")
print(f"R-squared score: {r2_score(y_test, predictions):.4f}")
