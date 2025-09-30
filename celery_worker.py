import time
from celery import Celery

celery = Celery(__name__, broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery.task
def generate_portfolio_report(portfolio_id: int, user_email: str):
    print(f"Generating portfolio report for portfolio {portfolio_id} and user {user_email}")
    # Simulating a long running task
    time.sleep(10)
    print(f"Portfolio report generated for portfolio {portfolio_id} and user {user_email}")
    return {"portfolio_id": portfolio_id, "user_email": user_email, "status": "complete"}