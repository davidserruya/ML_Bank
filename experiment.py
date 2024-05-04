import mlflow
# Restaurer une expérience supprimée
mlflow.set_tracking_uri(
    "https://user-ppeltier75-mlflow.user.lab.sspcloud.fr"
)
mlflow_experiment_name = "smartbank"
mlflow.set_experiment(experiment_name=mlflow_experiment_name)



