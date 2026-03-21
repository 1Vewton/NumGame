import logging
import os


def setup_logging():
    # logger
    logger = logging.getLogger("Logger")
    log_file = "app.log"

    # Create logs directory if it doesn't exist
    if not os.path.exists("../numgame/logs"):
        os.makedirs("../numgame/logs")

    # Configure logging to file
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s - %(name)s] - %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler(os.path.join("../numgame/logs", log_file)),
            logging.StreamHandler()  # Also log to console
        ]
    )
    logger.info("Logging setup complete.")
