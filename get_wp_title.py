import logging
import requests
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="vimeoUpload.log",
)

url = os.getenv("WP_API_URL") + "posts?categories=48&per_page=1"
username = os.getenv("WP_API_USER")
password = os.getenv("WP_API_PASSWORD")
headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }


def getPost(url):
    logging.info("Getting post from wordpress")
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        post = response.json()[0]
    else:
        logging.error(f"Error: {response.status_code} - {response.reason}")   

    return post     

def getName(url):
    logging.info("Getting file name from wordpress post")
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        study = response.json()[0]
        post_date = study['date']
        post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S").date()
        today = datetime.today().date()

        if post_date == today:
            post = response.json()
            post_title = post["title"]["rendered"]
            logging.info(post_title)
            return post_title
        else:
            logging.error("No post matching today's date found.")
            return str(today)

    else:
        logging.error(f"Error: {response.status_code} - {response.reason}")
