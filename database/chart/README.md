# Database Helm Chart

Runs a single Postgres Pod using the official `postgres` image. This chart is intended for development/testing and creates a single Pod (no Deployment/StatefulSet).

## Defaults

- Image: `postgres:15`
- DB name: `notesdb`
- User: `postgres`
- Password: `admin` (stored in a Kubernetes Secret created by the chart)

Install with defaults:

helm install database ./chart -n my-namespace --create-namespace

The chart creates a service with the same name as the release (e.g., `database`), you can connect other services using that service name:

helm install my-backend ./backend/chart -n my-namespace --set postgres.host=database

Notes:

- On first start Postgres will initialize the data directory and create the `notesdb` database (via `POSTGRES_DB` environment variable).
- For production, enable `persistence.enabled=true` and provide a PVC/storageClass and avoid checking secrets into `values.yaml`.
