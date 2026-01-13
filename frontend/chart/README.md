# Frontend Helm Chart

Deploys the frontend application using the image `ashiqa/ashiq-ar-devops-workflow-practice-frontend:latest`.

## Quickstart

Install the chart with default values:

helm install my-frontend ./chart -n my-namespace --create-namespace

To override the API host and port from `.env.example`:

helm install my-frontend ./chart -n my-namespace --set env.VITE_API_HOST="https://api.example.com" --set env.VITE_API_PORT="80"

To use a different image tag:

helm upgrade --install my-frontend ./chart -n my-namespace --set image.tag="v1.2.3"
