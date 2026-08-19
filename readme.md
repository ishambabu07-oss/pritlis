# Space Debris Dashboard

Monorepo for a CesiumJS dashboard, FastAPI orbital-analysis API, and ML risk pipeline.

## Setup and model workflow

Install the complete development environment with:

```bash
python3 -m pip install -r requirements.txt
```

## PostgreSQL

Create a PostgreSQL database and initialize its schema:

```bash
createdb -U postgres space_debris
psql -U postgres -d space_debris -f database/init_db.sql
export DATABASE_URL='postgresql+psycopg://postgres:postgres@localhost:5432/space_debris'
```

Set `DATABASE_URL` to the credentials for your deployment. The API verifies the
database connection and creates any missing tables during startup. Scan results
are stored in PostgreSQL and available from `GET /api/conjunctions`.

The API consumes `ml_pipeline/models/risk_xgboost_v1.pkl`. Model artifacts and
generated datasets are deliberately not committed, so build the local artifact
before starting the API:

```bash
python3 ml_pipeline/src/generate_data.py
python3 ml_pipeline/src/train_model.py
python3 ml_pipeline/src/evaluate.py
cd backend && uvicorn app.main:app --reload
```

For deployments, publish `risk_xgboost_v1.pkl` through the deployment artifact
process (or run the three pipeline commands during the build). Check
`GET /api/health` after startup: `risk_scoring_mode` must be `ml`. The API
will refuse to start if the trained model is unavailable, rather than silently
substituting heuristic scores.

`evaluate.py` is a synthetic-data regression check using the same held-out
split as training. It does not validate real collision risk; that requires a
representative, independently held-out conjunction dataset.
