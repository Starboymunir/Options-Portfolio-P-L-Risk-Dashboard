# Tasty Portfolio Dashboard

A Dash-based options portfolio dashboard that connects to the Tastytrade API, persists data in PostgreSQL/Aurora-compatible databases, and surfaces precise P&L and risk metrics.

## Features

- **Broker integration** – wraps the official [`tastytrade`](https://github.com/tastyware/tastytrade-api-python) client via `tasty_client` for session, positions, and activity data.
- **Database ready** – Aurora/PostgreSQL schema defined with SQLAlchemy models (`db/models.py`) and engine/session helpers (`db/session.py`).
- **Decimal-first analytics** – all calculations use `decimal.Decimal` helpers to avoid floating point drift (`analytics/utils.py`).
- **Portfolio insights** – compute per-position P&L, aggregate Greeks, and totals suitable for KPI cards and charts (`analytics/positions.py`).
- **Dash UI** – KPI cards, filters, equity curve, P&L by underlying chart, and a sortable/filterable positions table (`dashboard/layout.py`, `dashboard/callbacks.py`).

## Project structure

```
tasty-portfolio-dashboard/
  app.py
  requirements.txt
  .env.example
  tasty_client/
  db/
  analytics/
  dashboard/
```

See inline documentation in each module for implementation details.

## Precision handling

Financial calculations never use binary floats. The helpers in `analytics/utils.py` convert values to `Decimal` and enforce `getcontext().prec = 28`. Aggregations, P&L calculations, and Greek totals stay as `Decimal` until rendered, preventing penny drift that would otherwise accumulate in an options portfolio.

## Local development

1. **Clone & install**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Provision Postgres** – run a local Docker container or point to Supabase/Aurora.
   ```bash
   docker run --name tasty-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
   ```
3. **Configure environment** – copy `.env.example` to `.env` and fill in Tastytrade credentials plus the `DATABASE_URL`.
4. **Launch Dash**
   ```bash
   python app.py
   ```
   The dashboard loads mock data if the API is unreachable, making it easy to iterate on UI changes.

## Deployment ideas

- **Container** – package with the Python runtime, include migrations, and deploy to AWS ECS/Fargate.
- **PaaS** – run on Render/Fly/Heroku with a managed Postgres instance (Aurora, RDS, or Supabase) using the same SQLAlchemy models.
- **Serverless DB** – point the `DATABASE_URL` at Aurora Serverless v2 for production-grade availability without schema changes.

## Next steps

- Implement background jobs to sync Tastytrade data into Postgres on a schedule.
- Expand analytics to include realized P&L and rolling equity curves using the `trades` and `prices` tables.
- Add authentication and multi-account support for sharing the dashboard safely.

## Publishing to GitHub

If you cloned this repository locally but do not see commits on GitHub yet, double-check that you configured a remote and pushed
the latest work:

```bash
git remote -v             # verify the "origin" URL points at your GitHub repo
# if missing, add it:
git remote add origin git@github.com:YOUR_ORG/tasty-portfolio-dashboard.git
git push -u origin work   # push this branch ("work" by default) to GitHub
```

Once pushed, open a pull request from `work` (or your feature branch) into `main` to review the dashboard scaffold before deploying it.
