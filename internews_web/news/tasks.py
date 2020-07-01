from internews_web.celery import app
from logging import getLogger


logger = getLogger(__name__)


@app.task
def parse():
    logger.info("Test parsing...")
    print("Test parsing...")
