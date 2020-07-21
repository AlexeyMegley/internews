from logging import getLogger

from internews_web.celery import app
from .services import save_article

logger = getLogger(__name__)


@app.task
def parse():
    logger.info("Test parsing...")
    print("Test parsing...")

