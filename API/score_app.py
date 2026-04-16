import os
import mlflow
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_URI = os.getenv("MODEL_URI", "models:/churn_demo_model/1")


mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
if mlflow_tracking_uri:
    mlflow.set_tracking_uri(mlflow_tracking_uri)

mlflow_registry_uri = os.getenv("MLFLOW_REGISTRY_URI", "databricks")
mlflow.set_registry_uri(mlflow_registry_uri)

app = FastAPI(title="Churn Prediction API")

model = mlflow.pyfunc.load_model(MODEL_URI)

class PredictionRequest(BaseModel):
    industry: str | None = None
    country: str | None = None
    nps_score: float | None = None
    tenure_months: int | None = None
    monthly_contract_value: float | None = None
    login_count_30d: int | None = None
    feature_a_usage_30d: int | None = None
    feature_b_usage_30d: int | None = None
    storage_used_gb: float | None = None
    api_calls_30d: int | None = None
    invoice_amount: float | None = None
    paid_on_time: int | None = None
    days_late: int | None = None
    support_tickets_90d: int | None = None
    csat_score: float | None = None
    is_high_value_customer: int | None = None
    late_payment_risk: int | None = None
    low_engagement_risk: int | None = None
    support_risk: int | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        df = pd.DataFrame([request.model_dump()])

        int_cols = [
            "tenure_months",
            "login_count_30d",
            "feature_a_usage_30d",
            "feature_b_usage_30d",
            "api_calls_30d",
            "paid_on_time",
            "days_late",
            "support_tickets_90d",
            "is_high_value_customer",
            "late_payment_risk",
            "low_engagement_risk",
            "support_risk",
        ]

        float_cols = [
            "nps_score",
            "monthly_contract_value",
            "storage_used_gb",
            "invoice_amount",
            "csat_score",
        ]

        for col in int_cols:
            df[col] = pd.to_numeric(df[col], errors="raise").astype("int32")

        for col in float_cols:
            df[col] = pd.to_numeric(df[col], errors="raise").astype("float64")

        prediction = model.predict(df)
        return {"prediction": int(prediction[0])}

    except Exception as e:
        return {"error": str(e), "dtypes": {k: str(v) for k, v in df.dtypes.items()}}