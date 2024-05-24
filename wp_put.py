import logging
import requests
import os
import json
import datetime
from dotenv import load_dotenv
from vimeo_upload import getVideoInfo
from wp_get import getName, getPost


load_dotenv()
today = datetime.date.today()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="vimeoUpload.log",
)
# WP Login stuff
url = "https://northcountrychapel.com/wp-json/wp/v2"
username = os.getenv("WP_API_USER")
password = os.getenv("WP_API_PASSWORD")
headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


# Test video to upload
desktop = os.path.expanduser("~/Desktop")
video = desktop + "/thurber.eric.mp4"

# Get video to upload from local computer
def getUploadVideo():
    video_folder = r'\\Streaming-pc\d'
    available_files = os.listdir(video_folder)
    for file in available_files:
        file_path = os.path.join(video_folder, file)
        if os.path.isfile(file_path):
            created_date = datetime.date.fromtimestamp(os.path.getctime(file_path))
            if created_date == today:
                return file
            else: 
                logging.error("No available videos")

# Get title from WP post, video info from Vimeo
post_title = getName(os.getenv("WP_API_URL") + "posts?categories=48&per_page=1")
video_info = getVideoInfo(post_title)
video_id = video_info["uri"][-9:]

logging.debug(video_id)
logging.debug(video_info)

# Get embed code, title from vimeo
embed_code = video_info["embed"]["html"]
vimeo_title = video_info["title"]

logging.debug("Embed code: " + embed_code)
logging.debug("Title: " + vimeo_title)

# Update the contents of the WP post
post = getPost(os.getenv("WP_API_URL") + "posts?categories=48&per_page=1")
post_id = post["id"]
post_content = post["content"]
updated_content = post_content + "\n" + embed_code

payload = json.dumps({
  "content": updated_content
})

if vimeo_title == post_title:
    response = requests.put(f"{url}/posts/{post_id}", headers=headers, auth=(username, password), data=payload)

    


# def updatePost(id, payload):
#     response = requests.post(f"{url}/posts/{id}", headers=headers, auth=(username, password), data=payload)
#     print(response.content)