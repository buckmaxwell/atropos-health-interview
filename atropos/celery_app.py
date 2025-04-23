from celery import Celery

celery_app = Celery(
    "atropos",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",  # optional
)

# ⬇️ Force-import task modules to register them
import atropos.api.services.dispatch_task
