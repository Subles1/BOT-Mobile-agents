# P2P Rates Microservice

This microservice logs outgoing link clicks.

## Running

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the service:
```bash
uvicorn p2p_rates_service.main:app --reload
```

## Endpoints

- `GET /click?target_url=<url>&user_id=<user>` – Logs the click and redirects to the target URL.
- `GET /report` – Returns JSON statistics of clicks per user and URL.

## Reporting Script

Use `python -m p2p_rates_service.report` to print statistics from the database.
