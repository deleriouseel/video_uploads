import logging
import requests
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="studyDate.log",
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def getName(url):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        study = response.json()[0]
        post_date = study['date']
        post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S").date()
        today = datetime.today().date()

        if post_date == today:
            post = response.json()
            study = post["title"]["rendered"]
            logging.info(study)
            return study
        else:
            logging.info("No post matching today's date found.")
            return str(today)

    else:
        logging.error(f"Error: {response.status_code} - {response.reason}")
