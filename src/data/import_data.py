import os
import yaml
import pandas as pd

def import_yaml_config(filename: str = "toto.yaml") -> dict:
    dict_config = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as stream:
            dict_config = yaml.safe_load(stream)
    return dict_config


def import_data(path: str) -> pd.DataFrame:
    """Import CreditScore datasets
    Args:
        path (str): File location
    Returns:
        pd.DataFrame: CreditScore dataset
    """

    data = pd.read_csv(path)
    data = data.drop(columns=['ID','Customer_ID','Name','Credit_Mix','SSN','Type_of_Loan','Payment_of_Min_Amount'])
    return data
