"""A simple API to expose our trained RandomForest model for Tutanic survival."""
import requests
from fastapi import FastAPI
from joblib import load
from fastapi.openapi.docs import get_swagger_ui_html
import pandas as pd
import mlflow
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

# GET PRODUCTION MODEL -------------

model_name = "credit_score_model"
model_version = 1
model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")


# USE PRODUCTION MODEL IN APP ----------

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Prédiction d'ouverture de compte",
    description="<b>Application de prédiction d'ouverture d'un compte bancaire chez SmartBank",
    version="0.1.0"
)


# Page d'accueil
@app.get("/", tags=["Welcome"])
def show_welcome_page():
    """
    Affiche la page de bienvenue avec le nom et la version du modèle.
    """
    return {
        "Message": "API de prédiction de score de crédit",
        "Model_name": "CreditScore ML",
        "Model_version": "1.0",
    }

# Endpoint pour prédire la survie sur le Titanic
@app.get("/predict", tags=["Predict"])
async def predict(
    age: int = 35,
    annual_income: float = 50000,
    monthly_inhand_salary: float = 3000,
    num_bank_accounts: int = 2,
    num_credit_card: int = 3,
    interest_rate: float = 5.0,
    num_of_loan: int = 1,
    delay_from_due_date: int = 2,
    num_of_delayed_payment: int = 1,
    changed_credit_limit: float = 500,
    num_credit_inquiries: int = 1,
    outstanding_debt: float = 10000,
    credit_utilization_ratio: float = 0.30,
    credit_history_age: int = 5,
    total_emi_per_month: float = 300,
    amount_invested_monthly: float = 150,
    monthly_balance: float = 1000,
    interest_rate_x_outstanding_debt: float = 500,
    payment_behaviour: str = 'Low_spent_Small_value_payments',
    occupation: str = 'Engineer',
    month: int = 1
) -> str:
    """
    Endpoint pour prédire la survie sur le Titanic en fonction des caractéristiques fournies.
    """
    # Création du DataFrame avec les données fournies
    df = pd.DataFrame({
        "Age": [age],
        "Annual_Income": [annual_income],
        "Monthly_Inhand_Salary": [monthly_inhand_salary],
        "Num_Bank_Accounts": [num_bank_accounts],
        "Num_Credit_Card": [num_credit_card],
        "Interest_Rate": [interest_rate],
        "Num_of_Loan": [num_of_loan],
        "Delay_from_due_date": [delay_from_due_date],
        "Num_of_Delayed_Payment": [num_of_delayed_payment],
        "Changed_Credit_Limit": [changed_credit_limit],
        "Num_Credit_Inquiries": [num_credit_inquiries],
        "Outstanding_Debt": [outstanding_debt],
        "Credit_Utilization_Ratio": [credit_utilization_ratio],
        "Credit_History_Age": [credit_history_age],
        "Total_EMI_per_month": [total_emi_per_month],
        "Amount_invested_monthly": [amount_invested_monthly],
        "Monthly_Balance": [monthly_balance],
        "Interest_Rate_x_Outstanding_Debt": [interest_rate_x_outstanding_debt],
        "Payment_Behaviour": [payment_behaviour],
        "Occupation": [occupation],
        "Month": [month]
    })

    # Prédiction
    prediction_value = int(model.predict(df))
    if prediction_value == 0:
        prediction = "Poor"
    elif prediction_value == 1:
        prediction = "Standard"
    else:
        prediction = "Good"

    return prediction
