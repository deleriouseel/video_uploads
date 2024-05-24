import vimeo
import os
import wp_get
import re
import time
import logging
import datetime
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="vimeoUpload.log",
)

load_dotenv()
today = datetime.date.today()

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

#TODO: send getUploadVideo to uploadVimeo

def uploadVimeo(video):
  client = vimeo.VimeoClient(
      token=os.getenv('VIMEO_TOKEN'),
      key=os.getenv("VIMEO_KEY"),
      secret=os.getenv("VIMEO_SECRET"),
    )

  upload_name = wp_get.getName(os.getenv("WP_API_URL"))
  logging.info(f"Starting {video} upload")
  tags = ["northcountrychapel", "ncc", "biblestudy"]
  regex = r'\b(?:[1-3]?\s?[a-zA-Z]+\s?[A-Za-z]*)\b'
  book_name = re.search(upload_name, regex)

  uri = client.upload(video, data={
    'name': upload_name,
    'description': 'Join us as we study through the book of '+ str(book_name),
    'privacy': {
      'view': 'nobody' # prod = anybody
    },
    'content-rating': 'safe',
    "license":"by-nc-sa",
    "tags": tags, 
    })
  logging.info(f"Finished upload. Video uri is {uri}")
  return uri

def uploadCheck(uri):
  client = vimeo.VimeoClient(
      token=os.getenv('VIMEO_TOKEN'),
      key=os.getenv("VIMEO_KEY"),
      secret=os.getenv("VIMEO_SECRET"),
    )
  logging.info(f"Beginning upload check. {uri}")
  flag = False
  while flag == False: 
    response = client.get(uri + '?fields=upload.status').json()
    if response['upload']['status'] == 'complete':
      logging.info(f'Your video finished uploading. {response}')
      return True
    elif response['upload']['status'] == 'in_progress':
      logging.info('Your video is still uploading.')
      time.sleep(30)
      return False
    else:
      logging.info('Your video encountered an error during uploading.')
      #TODO: report error
      break
  logging.info(f"Finished upload check. The uri is: {uri}")  
  return uri  

def getVideoInfo(post_title):
  client = vimeo.VimeoClient(
      token=os.getenv('VIMEO_TOKEN'),
      key=os.getenv("VIMEO_KEY"),
      secret=os.getenv("VIMEO_SECRET"),
    )
  try:
    video_info = client.get(f"https://api.vimeo.com/users/75458348/videos?page=1&per_page=2&sort=date&query_fields=title&query={post_title}").json()
    if video_info["total"] != 0:
      return video_info
    else:
       logging.error("No video found")
  
  except:
    logging.error("Failed to retrieve video info")
