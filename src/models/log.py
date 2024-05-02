import mlflow
import os


def log_gsvc_to_mlflow(gscv, mlflow_experiment_name, application_number="appli21"):
    """Log a trained GridSearchCV object as an MLflow experiment."""
    mlflow.set_experiment(experiment_name=mlflow_experiment_name)

    for run_idx in range(len(gscv.cv_results_["params"])):
        run_name = f"run {run_idx}"
        with mlflow.start_run(run_name=run_name):
            # Log each hyperparameter combination
            params = gscv.cv_results_["params"][run_idx]
            for param in params:
                mlflow.log_param(param, params[param])

            # Log metrics like accuracy, precision, etc.
            scores = [score for score in gscv.cv_results_ if "mean_test" in score or "std_test" in score]
            for score in scores:
                mlflow.log_metric(score, gscv.cv_results_[score][run_idx])

            # Log the best model found in GridSearchCV as an artifact
            if run_idx == gscv.best_index_:
                mlflow.sklearn.log_model(gscv.best_estimator_, "best_model")

            # Log additional parameters specific to the application
            mlflow.log_param("application_number", application_number)
