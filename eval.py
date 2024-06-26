import pandas as pd
import mlflow
from sklearn.metrics import confusion_matrix, accuracy_score
from joblib import load

logged_model = "runs:/0796ef00e0ec48c8b1b1e5ed18ea4c93/gscv_model"

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
X_test = pd.read_csv("data/intermediate/X_test.csv")
y_test = pd.read_csv("data/intermediate/y_test.csv")

print(X_test.head())

y_test_predict = loaded_model.predict(X_test)

# EVALUATE ----------------------------

print(y_test_predict)

matrix = confusion_matrix(y_test, y_test_predict)

print("Accuracy:")
print(f"{accuracy_score(y_test, y_test_predict):.0%}")
print("Matrice de confusion:")
print(matrix)
