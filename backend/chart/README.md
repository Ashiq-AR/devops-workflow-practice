# Backend Helm Chart

Deploys the backend application using the image `ashiqa/ashiq-ar-devops-workflow-practice-backend:latest`.

## Quickstart

Install the chart with default values:

helm install my-backend ./chart -n my-namespace --create-namespace

The chart creates a Secret named `<release>-db` with the following keys:

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

Defaults are set in `values.yaml` to match `backend/models.py`, but **do not** store production secrets in `values.yaml`.

If you installed the database chart in the same namespace using the release name `database`, set `postgres.host=database` to connect to the database service created by that chart.

To override secrets at install-time (recommended):

helm upgrade --install my-backend ./chart -n my-namespace \
 --set postgres.host="db.example.com" \
 --set postgres.port="5432" \
 --set postgres.db="notesdb" \
 --set postgres.user="postgres" \
 --set postgres.password="supersecret"

To change image tag:

helm upgrade --install my-backend ./chart -n my-namespace --set image.tag="v1.2.3"
