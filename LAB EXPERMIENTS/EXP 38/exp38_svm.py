from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Create a binary classification dataset
X, y = make_classification(n_samples=100, n_features=2, n_classes=2, n_redundant=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Implement SVM
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

predictions = svm_model.predict(X_test)
print(f"SVM Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")