
# Snip: Distributed URL Shortener

Snip is a high-availability, distributed URL shortening service designed for scalability and speed. It utilizes a microservices architecture, leveraging a Twitter Snowflake-inspired algorithm for unique ID generation, Redis for sub-millisecond caching, and Nginx as a distributed load balancer.

**Live Demo:** [http://13.53.51.182](http://13.53.51.182)

---

## Architecture Overview

The system is designed to eliminate single points of failure and handle concurrent traffic across multiple instances.

* **API Gateway (Nginx):** Acts as a reverse proxy and load balancer, distributing traffic across backend workers and serving the static frontend.
* **Backend Workers (FastAPI):** Stateless Python instances that handle URL shortening logic and Snowflake ID generation.
* **Caching Layer (Redis):** Stores active URL mappings to prevent unnecessary database round-trips for frequent links.
* **Persistent Storage (Supabase):** A PostgreSQL-backed storage solution for long-term data retention.
* **Orchestration (Docker):** The entire stack is containerized for seamless deployment on cloud infrastructure.

---

## Tech Stack

* **Language:** Python 3.x
* **Web Framework:** FastAPI
* **Reverse Proxy / LB:** Nginx
* **Database:** Supabase (PostgreSQL)
* **In-Memory Cache:** Redis
* **Infrastructure:** Docker, AWS EC2 (Ubuntu)

---

## Features

* **Snowflake ID Generation:** Ensures collision-free, 64-bit unique identifiers across distributed machines without a central coordinator.
* **Base62 Encoding:** Converts large numeric IDs into short, URL-friendly alphanumeric strings.
* **Horizontal Scaling:** Capable of running multiple backend worker instances behind a single Nginx gateway.
* **High Availability:** Built-in health checks and container restarts via Docker Compose.
* **Responsive UI:** A dark-themed, minimalist dashboard for generating and managing links.

---

## Installation and Setup

### 1. Prerequisites
* Docker and Docker Compose installed.
* Active Supabase project with a `urls` table (columns: `id`, `short_code`, `long_url`).

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
MACHINE_ID=1
PUBLIC_URL=http://your_server_ip:8000/
````

### 3. Deploying with Docker

The fastest way to get the system running is using the pre-configured Docker Compose file:

```bash
# Clone the repository
git clone https://github.com/Koushal55/URLShortener.git
cd URLShortener

# Launch the distributed cluster
docker compose up -d --build
```

### 4. Verification

Once the containers are started, you can access the components at:

* **Frontend UI:** `http://your-ip`
* **Interactive API Docs:** `http://your-ip:8000/docs`

---

## API Endpoints

### Create Short URL

* **Endpoint:** `POST /shorten`
* **Request Body:** `{"long_url": "https://example.com"}`
* **Response:** JSON object containing the `short_code` and `short_url`.

### Resolve Short URL

* **Endpoint:** `GET /{short_code}`
* **Action:** Triggers a 302 Temporary Redirect to the destination URL.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.


