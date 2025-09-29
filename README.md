# Stock Portfolio Tracker API

A modern, fast, and secure FastAPI-based REST API for managing stock portfolios with real-time price tracking, user authentication, and Redis caching.

## 🚀 Features

- **User Authentication & Authorization**

  - JWT-based authentication with Argon2 password hashing
  - Secure user registration and login
  - Role-based access control

- **Portfolio Management**

  - Create and manage multiple portfolios
  - Track stock transactions (buy/sell)
  - Real-time stock price fetching with Redis caching
  - Portfolio performance analytics

- **Real-time Data**

  - Live stock price updates
  - Redis caching for improved performance
  - Configurable cache expiration

- **Database Integration**

  - PostgreSQL database with SQLAlchemy ORM
  - Docker-based PostgreSQL and Redis setup
  - Optimized queries and relationships

- **Security**
  - OAuth2 with JWT tokens
  - Argon2 password hashing (no 72-byte limit)
  - Environment-based configuration
  - Input validation with Pydantic

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.117+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2
- **Password Hashing**: Argon2 (via Passlib)
- **Caching**: Redis
- **Containerization**: Docker
- **Validation**: Pydantic v2
- **Python**: 3.13+

## 📋 Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose
- UV package manager (recommended) or pip

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/agajankush/stock_portfolio_tracker_fastapi
cd stock_portfolio_tracker_fastapi
```

### 2. Install Dependencies

Using UV (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

### 3. Start Docker Services

```bash
# Start PostgreSQL and Redis using Docker Compose
docker-compose up -d
```

### 4. Environment Setup

Create a `.env` file in the root directory:

```env
# Database Configuration (Docker PostgreSQL)
DATABASE_URL=postgresql://postgres:password@localhost:5432/stock_portfolio_db

# Redis Configuration (Docker Redis)
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
JWT_EXPIRATION_TIME=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 5. Start the Application

```bash
# Using UV
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000

## 🐳 Docker Setup

The project uses Docker for PostgreSQL and Redis services. Create a `docker-compose.yml` file:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: stock_portfolio_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Start the services:

```bash
docker-compose up -d
```

## 📚 API Endpoints

### Authentication

- `POST /users/` - Register a new user
- `POST /users/token` - Login and get access token

### Portfolios

- `GET /portfolios/` - Get user's portfolios
- `POST /portfolios/` - Create a new portfolio
- `GET /portfolios/{portfolio_id}` - Get specific portfolio
- `PUT /portfolios/{portfolio_id}` - Update portfolio
- `DELETE /portfolios/{portfolio_id}` - Delete portfolio

### Stock Data

- `GET /portfolios/stock/{ticker_symbol}/price` - Get real-time stock price
- `POST /portfolios/transactions/` - Add stock transaction
- `GET /portfolios/{portfolio_id}/transactions` - Get portfolio transactions

## 🔧 Configuration

### Environment Variables

| Variable              | Description                  | Default                    |
| --------------------- | ---------------------------- | -------------------------- |
| `DATABASE_URL`        | PostgreSQL connection string | Required                   |
| `REDIS_URL`           | Redis connection string      | `redis://localhost:6379/0` |
| `SECRET_KEY`          | JWT secret key               | Required                   |
| `ALGORITHM`           | JWT algorithm                | `HS256`                    |
| `JWT_EXPIRATION_TIME` | Token expiration in minutes  | `30`                       |
| `API_HOST`            | API host                     | `0.0.0.0`                  |
| `API_PORT`            | API port                     | `8000`                     |

### Database Configuration

The application uses PostgreSQL with the following main tables:

- `users` - User accounts and authentication
- `portfolios` - User portfolios
- `transactions` - Stock buy/sell transactions
- `stocks` - Stock information and metadata

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=.
```

## 📦 Development

### Project Structure

```
stock_portfolio_tracker_fastapi/
├── database/               # Database models and configuration
│   ├── models.py          # SQLAlchemy models
│   └── database.py        # Database connection
├── routers/               # API route handlers
│   ├── users.py          # User authentication routes
│   └── portfolios.py     # Portfolio management routes
├── schemas.py            # Pydantic models for API
├── security.py           # Authentication and security
├── redis_client.py       # Redis connection and utilities
├── main.py              # FastAPI application entry point
├── docker-compose.yml   # Docker services configuration
├── pyproject.toml       # Project dependencies and metadata
└── README.md            # This file
```

### Adding New Features

1. **Database Changes**: Update models in `database/models.py` (manual schema changes for now)
2. **API Endpoints**: Add new routes in the appropriate router file
3. **Validation**: Update schemas in `schemas.py` for new data models
4. **Authentication**: Use the existing OAuth2 system for protected endpoints

### Code Style

- Follow PEP 8 guidelines
- Use type hints throughout
- Document functions and classes
- Write tests for new features

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.13-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

- Use environment variables for all secrets
- Set up proper logging
- Configure reverse proxy (nginx)
- Set up monitoring and health checks
- Use production-grade database and Redis instances
- Enable HTTPS/TLS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🔮 Roadmap

- [ ] Real-time WebSocket connections for live updates
- [ ] Advanced portfolio analytics and reporting
- [ ] Integration with multiple stock data providers
- [ ] Mobile app API endpoints
- [ ] Automated trading strategies
- [ ] Social features (portfolio sharing)
- [ ] Advanced caching strategies
- [ ] Performance monitoring and metrics

---

**Built with ❤️ using FastAPI, PostgreSQL, and Redis**
