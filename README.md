# Real-Time Stock Portfolio Tracker API

A high-performance, asynchronous API built with FastAPI to manage user stock portfolios, featuring real-time price updates via WebSockets, background task processing, and a complete observability stack.

---

## Core Technologies

| Technology         | Purpose                                                             |
| :----------------- | :------------------------------------------------------------------ |
| **FastAPI**        | High-performance Python web framework for building the API.         |
| **PostgreSQL**     | Relational database for persistent data storage.                    |
| **SQLAlchemy**     | Python ORM for interacting with the PostgreSQL database.            |
| **Redis**          | In-memory database used for caching and as a Celery message broker. |
| **Celery**         | Distributed task queue for handling background processes.           |
| **WebSockets**     | For real-time, bidirectional communication with clients.            |
| **OpenTelemetry**  | For generating traces, metrics, and logs for observability.         |
| **Jaeger**         | To visualize distributed traces.                                    |
| **Docker**         | For containerizing the application and its services.                |
| **Pytest**         | For running automated tests.                                        |
| **GitHub Actions** | For CI/CD automation.                                               |
| **Ruff**           | For code linting and formatting.                                    |

---

## Features

- **User Authentication**: Secure user registration and JWT-based authentication.
- **Database Integration**: Robust data persistence using PostgreSQL and SQLAlchemy.
- **Real-Time Updates**: Live stock price updates pushed to clients via WebSockets.
- **Caching**: Redis caching layer to reduce latency and external API calls.
- **Background Tasks**: Asynchronous report generation using Celery.
- **Observability**: Full instrumentation with structured logging, Prometheus metrics, and distributed tracing with OpenTelemetry and Jaeger.
- **CI/CD**: Automated testing pipeline using GitHub Actions.
- **Containerized**: Fully containerized services for consistent development and deployment environments.

---

## Getting Started

### Prerequisites

- Git
- Python 3.11+
- Docker and Docker Compose

### Local Setup

1.  **Clone the repository:**

    ```shell
    git clone https://github.com/agajankush/stock_portfolio_tracker_fastapi.git
    cd stock_portfolio_tracker_fastapi
    ```

2.  **Create and activate the virtual environment:**

    ```shell
    # Using uv
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```shell
    uv pip install -r requirements.txt
    ```

4.  **Start the services (Database, Redis, Jaeger):**

    ```shell
    docker run --name portfolio-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=portfoliodb -p 5432:5432 -d postgres
    docker run --name portfolio-redis -p 6379:6379 -d redis
    docker run --name jaeger -p 16686:16686 -p 4317:4317 -d jaegertracing/all-in-one:latest
    ```

5.  **Run the application:**

    ```shell
    # Run the FastAPI server
    uvicorn main:app --reload

    # In a new terminal, run the Celery worker
    celery -A celery_worker.celery worker --loglevel=info
    ```

    The API will be available at `http://localhost:8000`.

### Running Tests

To run the automated tests, use `pytest`:

```shell
pytest
```
