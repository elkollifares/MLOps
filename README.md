# Churn Prediction API (MLOps on AKS)

This project deploys a machine learning model as a REST API using FastAPI, Databricks (MLflow), Docker, Azure Container Registry, Azure Kubernetes Service, and Azure DevOps.


## Architecture

Databricks (MLflow Model Registry)
→ Docker Image
→ Azure Container Registry (ACR)
→ Azure DevOps Pipeline
→ Azure Kubernetes Service (AKS)
→ FastAPI API


## Project Structure

API/
  app/                # FastAPI code
  Dockerfile          # Container build
  aks/deployment.yaml # Kubernetes config

azure-pipelines.yaml  # CI/CD pipeline


## Prerequisites

- Azure subscription
- AKS cluster
- Azure Container Registry
- Databricks workspace
- MLflow model registered
- kubectl installed


## Configuration

The API uses the following environment variables:

- MODEL_URI=models:/churn_demo_model/1
- MLFLOW_REGISTRY_URI=databricks
- DATABRICKS_HOST=<your-url>
- DATABRICKS_TOKEN (stored in Kubernetes secret)


## Deployment

1. Create Databricks secret:

kubectl create secret generic databricks-secret \
  --from-literal=token=<YOUR_TOKEN>

2. Apply Kubernetes manifests:

kubectl apply -f API/aks/deployment.yaml

3. Get external IP:

kubectl get svc churn-api-service

## CI/CD Pipeline

The Azure DevOps pipeline:

- Reads image tag from deployment.yaml
- Deploys to AKS using KubernetesManifest task
- Uses service connections for Azure and Kubernetes


## API Usage

curl http://<EXTERNAL-IP>/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [...]}'

  {
  "industry": "Retail",
  "country": "France",
  "nps_score": 7.5,
  "tenure_months": 14,
  "monthly_contract_value": 120.0,
  "login_count_30d": 9,
  "feature_a_usage_30d": 12,
  "feature_b_usage_30d": 5,
  "storage_used_gb": 20.5,
  "api_calls_30d": 110,
  "invoice_amount": 130.0,
  "paid_on_time": 1,
  "days_late": 0,
  "support_tickets_90d": 1,
  "csat_score": 4.2,
  "is_high_value_customer": 1,
  "late_payment_risk": 0,
  "low_engagement_risk": 0,
  "support_risk": 0
}

## Local Development

docker build -t churn-api .
docker run -p 8000:8000 churn-api


## Troubleshooting

kubectl get pods
kubectl logs <pod-name>
kubectl describe deployment churn-api


## Improvements

- Add autoscaling (HPA)
- Use Helm charts
- Integrate Azure Key Vault
- Add monitoring (Prometheus/Grafana)


## Infrastructure Deployment with Terraform

The cloud infrastructure for this project can be provisioned with Terraform. This includes the resource group, Azure Container Registry (ACR), Azure Kubernetes Service (AKS), networking, and any supporting Azure resources required for deployment.

### What Terraform Deploys

Terraform is used to create and manage:

- Resource Group
- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Virtual Network and Subnets
- Managed Identity or Service Principal access
- Optional monitoring and logging resources

### Prerequisites

Before deploying infrastructure, make sure you have:

- Azure subscription
- Terraform installed
- Azure CLI installed
- Sufficient permissions to create Azure resources

Check versions:

```bash
terraform -version
az version


terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── provider.tf
├── terraform.tfvars