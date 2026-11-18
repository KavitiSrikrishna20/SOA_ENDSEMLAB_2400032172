# Multiple-Container Infrastructure Setup & Deployment Using Docker Compose

## Aim

Build and run a Flask REST API and a Redis cache as two communicating Docker
containers managed by Docker Compose. The API stores a message in Redis,
retrieves it, and returns it as JSON.

## Software requirements

- Docker Desktop with the Docker Engine running
- Docker Compose v2 (`docker compose`)
- curl or a web browser for the API test

## Project structure

```text
docker-compose-demo/
├── app.py
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```

## File descriptions

- `app.py` defines `GET /api/data`, stores and retrieves the message in Redis,
  and returns a JSON response. Flask listens on `0.0.0.0:5000` inside its
  container.
- `requirements.txt` lists Flask and the Python Redis client.
- `Dockerfile` builds the API image using Python 3.11 slim.
- `compose.yaml` configures the API and Redis services on Compose's default
  network.
- `README.md` contains the lab setup and execution instructions.

## Docker Compose configuration

Compose builds the `api` service from the local Dockerfile, maps host port
`8050` to container port `5000`, and sets `REDIS_HOST=redis`. The API uses the
Compose service name `redis` to reach Redis on port `6379`. Compose waits for
Redis's health check to pass before starting the API. Redis port `6379` is
exposed to the other Compose service; it is not published to the host.

## Execution commands

Open a terminal in this project folder and check Docker and Compose:

```powershell
docker --version
docker compose version
```

Build the API image and start both containers in the background:

```powershell
docker compose up --build -d
```

Confirm both containers are running:

```powershell
docker ps
```

The `STATUS` column should show `Up` for `flask_api` and `redis_db`.

## Testing procedure

Request the API using curl:

```powershell
curl.exe http://localhost:8050/api/data
```

Or open <http://localhost:8050/api/data> in a browser. The endpoint writes the
message to Redis and reads it back before returning the response.

Expected JSON response:

```json
{
  "message": "Hello from Docker Compose",
  "status": "Success"
}
```

To inspect service logs if the request fails:

```powershell
docker compose logs api
docker compose logs redis
```

## Troubleshooting

- If Docker reports `failed to connect to the docker API` or
  `dockerDesktopLinuxEngine` is missing, Docker Desktop is not running or its
  engine has not finished starting. Open Docker Desktop, wait until it reports
  that the engine is running, then confirm with `docker info` and retry
  `docker compose up --build -d`.
- If curl reports `Empty reply from server` immediately after startup, the API
  may still be starting. Check `docker compose logs api`, wait for Flask's
  `Running on all addresses (0.0.0.0)` message, and retry the request.

After making code or configuration changes, rebuild and restart the services:

```powershell
docker compose up --build -d
```

## Cleanup

Stop and remove the containers and the Compose network:

```powershell
docker compose down
```

## Result

When the API returns the expected JSON and both containers show `Up` in
`docker ps`, the Flask-to-Redis communication experiment is successful.
