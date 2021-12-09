import logging
import os

from dotenv import load_dotenv

load_dotenv()
from app.run import run


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)

    run(os.getenv('TOKEN'))
