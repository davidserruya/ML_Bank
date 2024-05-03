# ML_Bank [![Construction image Docker](https://github.com/marco-samori/ML_Bank/actions/workflows/prod.yml/badge.svg)](https://github.com/marco-samori/ML_Bank/actions/workflows/prod.yml) <img src="https://camo.githubusercontent.com/6c98e3ffde19edc990fdc90b500adc614226e333a73b20c7b0fbb52d29c95de8/68747470733a2f2f75706c6f61642e77696b696d656469612e6f72672f77696b6970656469612f636f6d6d6f6e732f7468756d622f652f65632f4c4f474f2d454e5341452e706e672f39303070782d4c4f474f2d454e5341452e706e67" alt="Description de l'image" width="200"/>

## Topic</a>

An application of a fictitious online bank called SmartBank, which allows checking the eligibility of a customer to open an account by answering a form. We test their eligibility using an XGBoost machine learning model.

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Structure](#structure)
4. [Model Used](#model-used)
5. [Demonstration](#demonstration)
6. [Reusability](#reusability)
7. [Contributors](#contributors)

## Introduction <a name="introduction"></a>

This project centers on SmartBank, a fictional online banking application designed to assess customer eligibility for account opening. Utilizing the XGBoost machine learning algorithm, SmartBank evaluates user-provided financial information to determine eligibility. The project progresses from development to production, culminating in the deployment of a Streamlit web application interface. This interface streamlines the eligibility assessment process, enabling users to interact seamlessly with SmartBank and receive prompt results. The project highlights the integration of machine learning models into real-world applications, prioritizing usability and accessibility for users.


## Prerequisites <a name="prerequisites"></a>

To use this project, it is recommended to create a config.yaml file with the following structure::

```yaml
jeton_api: ####
train_path: ####
test_path: ####
test_fraction: ####
```
## Structure <a name="structure"></a>
``` bash
project_root/
│
├── data/
│   ├── train.csv
│   └── test.csv
│
├── models/
│   ├── model.pkl
│   └── model_metadata.json
│
├── notebooks/
│   ├── data_exploration.ipynb
│   └── model_training.ipynb
│
├── src/
│   ├── data/
│   │   ├── import_data.py
│   │   └── preprocess_data.py
│   │
│   ├── models/
│   │   └── train_model.py
│   │
│   └── utils/
│       └── helper_functions.py
│
├── README.md
├── requirements.txt
└── config.yaml
```
## Model Used <a name="model-used"></a>

For our project, we utilized an XGBoost model to predict the credit scores of bank clients. XGBoost is a highly effective machine learning algorithm well-suited for classification and regression tasks.

In our case, we also employed a Synthetic Minority Over-sampling Technique (SMOTE) to address class imbalance by oversampling the minority class in our dataset. This helped improve model performance by tackling the class imbalance issue.

Furthermore, we employed grid search with cross-validation to search for the best hyperparameters for the XGBoost model. Cross-validation allowed us to robustly evaluate model performance by using multiple data subsets for training and validation.

## Demonstration <a name="demonstration"></a>

Discover the model interactively on [this website](https://ensae-reproductibilite.github.io/application-correction/) 
or through the [API](https://titanic.kub.sspcloud.fr/docs).

## Reusability <a name="reusability"></a>

To test this project, the following code is sufficient:

```python
pip install -r requirements.txt
python main.py
```

## Contributors <a name="contributors"></a>
- David Serruya
- Paul Peltier
- Marco Samori
