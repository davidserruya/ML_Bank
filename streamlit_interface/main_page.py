from ctypes import alignment
import streamlit as st  
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import streamlit.components.v1 as components
import pandas as pd
from streamlit_option_menu import option_menu
import requests
import os

# Settings
st.set_page_config(layout="wide")
st.markdown(""" <style> .block-container {padding-top: 2.5rem; padding-bottom: 0rem;} </style> """, unsafe_allow_html=True)


# Fonction pour envoyer une requête à l'API et afficher la réponse
def call_api(data):
    api_url = "https://smartbank.kub.sspcloud.fr/predict"
    response = requests.get(api_url, params=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        st.write("Erreur lors de l'appel à l'API")
        return None

#Functions of navbar menu
def do_home():
    # Lire le contenu du fichier home_page.html
    with open("streamlit_interface/home_page.html", 'r', encoding='utf-8') as HtmlFile:
        source_code = HtmlFile.read()
    # Afficher le code HTML dans Streamlit
    components.html(source_code, height=1300) 


def do_form():
  result=None
  payment_behaviour_options = [
    'High_spent_Small_value_payments',
    'Low_spent_Large_value_payments',
    'Low_spent_Medium_value_payments',
    'Low_spent_Small_value_payments',
    'High_spent_Medium_value_payments',
    'High_spent_Large_value_payments']

  col1, col2 = st.columns([1,1])
  with col1:
    with st.form("my_form"):
         st.markdown("<h1 style='text-align: center;padding-top:0rem'>Vérifiez votre éligibilité</h1>", unsafe_allow_html=True)
         age = st.number_input('Âge :',min_value=0)
         annual_income = st.number_input('Revenu annuel :',min_value=0)
         monthly_inhand_salary = st.number_input('Salaire net mensuel :',min_value=0)
         num_bank_accounts = st.number_input('Nombre de comptes bancaires :',min_value=0)
         num_credit_card = st.number_input('Nombre de cartes de crédit :',min_value=0)
         interest_rate = st.number_input('Taux d\'intérêt :',min_value=0,max_value=100)
         num_of_loan = st.number_input('Nombre de prêts :',min_value=0)
         delay_from_due_date = st.number_input('Délai depuis la date d\'échéance :',min_value=0)
         num_of_delayed_payment = st.number_input('Nombre de paiements en retard :',min_value=0)
         changed_credit_limit = st.number_input('Limite de crédit modifiée :',min_value=0)
         num_credit_inquiries = st.number_input('Nombre de demandes de crédit :',min_value=0)
         outstanding_debt = st.number_input('Dette en cours :',min_value=0)
         credit_utilization_ratio = st.number_input("Ratio d'utilisation du crédit :",min_value=0,max_value=100)
         credit_history_age = st.number_input("Âge de l'historique de crédit :",min_value=0)
         total_emi_per_month = st.number_input('Total des mensualités par mois :',min_value=0)
         amount_invested_monthly = st.number_input('Montant investi mensuel :',min_value=0)
         monthly_balance = st.number_input('Solde mensuel :',min_value=0)
         interest_rate_x_outstanding_debt = interest_rate * outstanding_debt
         payment_behaviour = st.selectbox('Comportement de paiement :', payment_behaviour_options)
         occupation = st.text_input("Métier :")
         month = st.selectbox('Mois de la demande :', list(range(1, 13)), index=0)

         # Every form must have a submit button.
         submitted = st.form_submit_button("Submit")
         if submitted:
            df = {
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
            }
            result=call_api(df)
          
    with col2:
        col3, col4, col5 = st.columns([1,6,1])

        with col4:
            if result is not None:
                if result == 'Poor':
                    title='Désolé'
                    message="Nous sommes désolés, mais sur la base de votre dossier actuel, nous ne pouvons pas donner suite à votre demande pour le moment."
                    button="Découvrir SmartBank"
                elif result == "Standard":
                    title='En cours de traitement'
                    message="Votre demande est en cours de traitement. Nous aimerions échanger davantage avec vous pour mieux comprendre vos besoins. Un de nos représentants prendra contact avec vous sous peu."
                    button="Contactez nous"
                elif result == "Good":
                    st.balloons()
                    title='Binvenue Chez SmartBank'
                    message="Félicitations! Vous êtes éligible pour devenir un nouveau client chez SmartBank. Vous recevrez sous peu un e-mail détaillant la procédure à suivre pour finaliser l'ouverture de votre compte."
                    button="Contactez nous"
            
                with open("streamlit_interface/contact_us.html", "r") as file:
                    html_content = file.read()

                # Remplacement des balises spéciales par les valeurs correspondantes
                html_content = html_content.replace("{title}", title)
                html_content = html_content.replace("{message}", message)
                html_content = html_content.replace("{button}", button)

                # Écriture du contenu mis à jour dans un nouveau fichier HTML
                with open("streamlit_interface/contact_us_new.html", "w") as file:
                    file.write(html_content)
                
                with open("streamlit_interface/contact_us_new.html", 'r', encoding='utf-8') as HtmlFile:
                    source_code_form = HtmlFile.read()
                # Afficher le code HTML dans Streamlit
                components.html(source_code_form,height=800) 
            else:
                st.write("")



# Display navbar menu 
selected = option_menu(None, ["Home", "Form"], 
    icons=['house', "bi bi-file-earmark-text"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "icon": {"color": "black", "font-size": "30px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#f4f4f4"},
        "nav-link-selected": {"background-color": "#dcdcdc","color":"black"}
    }) 

if selected=='Home':
    do_home()

else:
    do_form()
    







