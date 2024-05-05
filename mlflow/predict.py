import mlflow
import pandas as pd


model_name = "smartbank"
model_version = 2

loaded_model = mlflow.pyfunc.load_model(
    "runs:/0796ef00e0ec48c8b1b1e5ed18ea4c93/best_model"
)

def create_data(
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
    occupation: str = 'Engineer',
    month: int = 1,
    payment_behaviour: str = 'Low_spent_Small_value_payments'
) -> str:
    """
    """

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
        "Occupation": [occupation],
        "Month": [month],
        "Payment_Behaviour": [payment_behaviour]
    })

    return df



data = pd.concat([
    create_data(),
    create_data(age=45, annual_income=75000)
])

print(
    loaded_model.predict(pd.DataFrame(data))
)