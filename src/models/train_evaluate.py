import pandas as pd

from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTENC
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import xgboost as xgb


def split_train_test_mep(data: pd.DataFrame, fraction_test: float = 0.1):
    """Split Titanic dataset in train and test sets

    Args:
        data (pd.DataFrame): Titanic dataset
        y_index (int, optional): Positional index for target variable.
        fraction_test (float, optional):
            Fraction of observation dedicated to test dataset.
            Defaults to 0.1.

    Returns:
        Four elements : X_train, X_test, y_train, y_test
    """

    train = data.sample(frac=1 - fraction_test, random_state=435)
    test = data.drop(train.index)

    return train, test





def build_pipeline(numeric_features=['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card',
                                     'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit',
                                     'Num_Credit_Inquiries', 'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age',
                                     'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance'],
                    categorical_features=['Occupation', 'Month', 'Payment_Behaviour'],
                    n_trees=300):
    """
    XGBoost for Credit Score

    Args:
        numeric_features (list, optional): List of numerical feature names.
        categorical_features (list, optional): List of categorical feature names.
        n_trees (int, optional): Number of trees for XGBoost classifier.

    Returns:
        sklearn.pipeline.Pipeline: Configured processing and classification pipeline.
    """

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", MinMaxScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder()),
        ]
    )

    # Index mapping for categorical features to use in SMOTENC
    X = pd.DataFrame(columns=numeric_features + categorical_features)  # Mock to generate column indices
    categorical_indices = [X.columns.get_loc(name) for name in categorical_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("Preprocessing numerical", numeric_transformer, numeric_features),
            ("Preprocessing categorical", categorical_transformer, categorical_features),
        ]
    )

    pipe = ImbPipeline(
        [
            ('smote', SMOTENC(categorical_features=categorical_indices, random_state=42, k_neighbors=3)),
            ('preprocessor', preprocessor),
            ('classifier', xgb.XGBClassifier(n_estimators=n_trees, eval_metric='mlogloss'))
        ]
    )

    return pipe