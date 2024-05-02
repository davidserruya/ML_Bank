import pandas as pd



def create_interaction_feature(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new feature by interacting two existing features.
    Args:
        df (pd.DataFrame): The dataset where the new feature will be added.
    
    Returns:
        pd.DataFrame: Dataset with the new interaction feature added.
    """
    data['Interest_Rate_x_Outstanding_Debt'] = data['Interest_Rate'] / 100 * data['Outstanding_Debt']
    return data


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the dataset for credit score prediction.
    Args:
        df (pd.DataFrame): The dataset to preprocess.
    
    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    # Dropping rows where the target variable is missing
    data = data.dropna(subset=['Credit_Score'])
    # Dropping irrelevant columns
    data = data.drop(['ID', 'Customer_ID', 'Name', 'Credit_Mix', 'Credit_Score', 'SSN', 'Type_of_Loan', 'Payment_of_Min_Amount'], axis=1)
    return data

def feature_engineering(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply our feature engineering pipeline for credit scoring.

    Args:
        data (pd.DataFrame): Initial dataframe.

    Returns:
        pd.DataFrame: Dataframe with feature engineering being handled.
    """
    data_training  = preprocess_data(data)
    data_training  = create_interaction_feature(data_training )
    return data_training 
