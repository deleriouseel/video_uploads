import logging
import requests
import os
import json
import datetime
import re
from dotenv import load_dotenv
from vimeo_upload import getVideoInfo, uploadCheck, getUploadVideo, uploadVimeo
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
def updatePost():
    """Update a WordPress post with Vimeo video iframe.

    This fetches info about the latest WordPress post from the "bible study" category,
    uploads a video file to Vimeo, retrieves the iframe content for the uploaded video,
    and updates the WordPress post with the video embed code if the post's date matches today's date.
    """

    try:
        # Get WP info
        post = getPost(os.getenv("WP_API_URL") + "posts?categories=48&per_page=1")
        if post is None:
            logging.error("Failed to retrieve post from WordPress API")
            return None, None
        #Get video location
        upload_file = getUploadVideo()
        if upload_file:
            logging.info(f"Video file to upload: {upload_file}")
        else:
            logging.error("No video file found.")

        # Upload video
        uri = uploadVimeo(upload_file)

        # Check upload succeeded
        uploadCheck(uri)
        video_info = getVideoInfo(uri)
       

        # Get date from WP post
        post_date = post["date"][0:10]
        post_title = post["title"]["rendered"]

        logging.debug(f"Post date: {post_date}")
        logging.debug(f"Post title: {post_title}")

        # Get video id, embed code, title from Vimeo
        video_id = video_info["uri"][-9:]
        embed_code = video_info["embed"]["html"]
        vimeo_title = video_info["name"]

        logging.debug(f"Video ID: {video_id}")
        logging.debug(f"Embed code: {embed_code}")
        logging.debug(f"Video Title: {vimeo_title}")

        post_id = post["id"]
        post_content = post["content"]["rendered"]
        post_content= re.sub(r'[\r\n]+', '\n', post_content)

        payload = json.dumps({
            "content": post_content + embed_code
            })
        

        if vimeo_title == post_title:
            response = requests.put(f"{url}posts/{post_id}", headers=headers, auth=(username, password), data=payload)
            logging.info(f"Post updated successfully: {response.text}")
        else:
            logging.debug("Titles don't match")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")   

   
updatePost()
