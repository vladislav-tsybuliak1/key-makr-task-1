import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="log_analyzer.log", mode="a"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)
