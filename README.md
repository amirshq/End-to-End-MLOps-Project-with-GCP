# End to End MLOps Project with GCP
gcloud builds submit --tag gcr.io/end-to-end-mlops-using-gcp/index
gcloud run deploy --image gcr.io/end-to-end-mlops-using-gcp/index --platform managed

