# Flask Hello World with Tailwind and Docker

This repository contains a simple Python Flask application that renders a
"Hello World" page using a template. Tailwind CSS is included via CDN.

## Project layout

```
Docker/
├── app/
│   ├── app.py
│   └── templates/
│       └── index.html
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── start.sh
└── .gitignore
```

## Setup (local development)

1. Create a virtual environment (venv):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   > **Note:** On Debian/Ubuntu you may need to install `python3-venv` first
   > (`sudo apt install python3-venv`).

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   export FLASK_APP=app/app.py
   flask run --host=0.0.0.0 --port=5000
   ```

4. Open [http://localhost:5000](http://localhost:5000) to see the page.

## Docker

The `Dockerfile` builds an image that includes:

- Python 3.11 with the Flask application
- `nginx` configured as a reverse proxy
- `redis-server` and `mongodb` installed and started

A `docker-compose.yml` is also provided to bring up the services:

```bash
docker compose up --build
```

This will expose:

- `8080` → Nginx/Flask (mapped from host to container port 80)
- `6379` → Redis
- `27017` → MongoDB

The `start.sh` script handles starting all services within the container.

## Tailwind CSS

The HTML template (`app/templates/index.html`) pulls Tailwind from the
official CDN; no build step is required.

---

Feel free to extend the application or split services into separate
containers if needed.  :rocket: