"""
Prediction de la survie d'un individu sur le CreditScore
"""

# GESTION ENVIRONNEMENT --------------------------------

from pathlib import Path
import argparse
from joblib import dump
from sklearn.model_selection import GridSearchCV

import src.data.import_data as imp
import src.features.build_features as bf
import src.models.log as mlog
import src.models.train_evaluate as te


# PARAMETRES -------------------------------

# Paramètres ligne de commande
parser = argparse.ArgumentParser(description="Paramètres du XGBoost")
parser.add_argument("--n_trees", type=int, default=300, help="Nombre d'arbres")
parser.add_argument("--appli", type=str, default="appli21", help="Application number")
args = parser.parse_args()

# Paramètres YAML
config = imp.import_yaml_config("configuration/config.yaml")
base_url = (
    "https://minio.lab.sspcloud.fr/marcosamori/creditscore/data/raw/"
)
API_TOKEN = config.get("jeton_api")
LOCATION_TRAIN = config.get("train_path")
LOCATION_TEST = config.get("test_path")
TEST_FRACTION = config.get("test_fraction")
N_TREES = args.n_trees
APPLI_ID = args.appli
EXPERIMENT_NAME = "CreditScoreExperiment"

# FEATURE ENGINEERING --------------------------------

credit_raw = imp.import_data(LOCATION_TRAIN)

# Create a 'Title' variable
credit_intermediate = bf.feature_engineering(credit_raw)


train, test = te.split_train_test_mep(
    credit_intermediate, fraction_test=TEST_FRACTION
)
X_train, y_train = train.drop("Credit_Score", axis="columns"), train["Credit_Score"]
X_test, y_test = test.drop("Credit_Score", axis="columns"), test["Credit_Score"]


def log_local_data(data, filename):
    data.to_csv(f"data/intermediate/{filename}.csv", index=False)


output_dir = Path("data/intermediate")
output_dir.mkdir(parents=True, exist_ok=True)

log_local_data(X_train, "X_train")
log_local_data(X_test, "X_test")
log_local_data(y_train, "y_train")
log_local_data(y_test, "y_test")


# MODELISATION: XGBOOST ----------------------------

pipe = te.build_pipeline(numeric_features=['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card',
                                     'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit',
                                     'Num_Credit_Inquiries', 'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age',
                                     'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance'],
                    categorical_features=['Occupation', 'Month', 'Payment_Behaviour'],
                    n_trees=300)

param_grid = {
    'smote__k_neighbors': [3, 5, 7],
    'classifier__max_depth': [3, 5, 7],
    'classifier__learning_rate': [0.01, 0.1, 0.2],
    'classifier__n_estimators': [100, 200, 300],
    'classifier__subsample': [0.8, 1]
}


pipe_cross_validation = GridSearchCV(
    pipe, 
    param_grid=param_grid, 
    cv=5, 
    scoring=["accuracy", "precision", "recall", "f1"],
    refit="accuracy",
    verbose=1, 
    n_jobs=-1
)

pipe_cross_validation.fit(X_train, y_train)

mlog.log_gsvc_to_mlflow(pipe_cross_validation, EXPERIMENT_NAME, APPLI_ID)

pipe = pipe_cross_validation.best_estimator_

dump(pipe, "model.joblib")
