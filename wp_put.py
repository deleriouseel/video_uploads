import logging
import requests
import os
import json
import datetime
from dotenv import load_dotenv
from vimeo_upload import getVideoInfo
from wp_get import getPost


load_dotenv()
today = str(datetime.date.today())

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="vimeoUpload.log",
)
# WP Login stuff
url = os.getenv("WP_API_URL")
username = os.getenv("WP_API_USER")
password = os.getenv("WP_API_PASSWORD")
headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

#TODO: Check if video has finished uploading


# Get title, date from WP post
post = getPost(os.getenv("WP_API_URL") + "posts?categories=48&per_page=1")
post_title = post["title"]
post_date = post["date"][0:10]

# Get video id, embed code, title from Vimeo
video_info = getVideoInfo(post_title)
video_id = video_info["uri"][-9:]
embed_code = video_info["embed"]["html"]
vimeo_title = video_info["title"]

logging.debug("Video ID: " + video_id)
logging.debug("Embed code: " + embed_code)
logging.debug("Title: " + vimeo_title)

# Update the contents of the WP post
if post_date == today:
        post_title = post["title"]["rendered"]
        post_id = post["id"]
        post_content = post["content"]
        updated_content = post_content,"/n",embed_code

        payload = json.dumps({
        "content": updated_content
        })
        if vimeo_title == post_title:
            response = requests.put(f"{url}/posts/{post_id}", headers=headers, auth=(username, password), data=payload)
            
        else:
             logging.error("Titles don't match")
else:
    logging.error("No post matching today's date found. Returning today's date.")

