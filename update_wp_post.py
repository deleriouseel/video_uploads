import logging
import requests
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="updateWP.log",
)

#TODO: log in to wp
#TODO: get correct post to update
#TODO: get vimeo embed
#TODO: update post