import vimeo
import os
import re
import time
import logging
import datetime
from dotenv import load_dotenv
from wp_get import getPost, getName

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="vimeoUpload.log",
)

load_dotenv()
today = datetime.date.today()

def getUploadVideo():
    logging.debug("Starting getUploadVideo")
    video_folder = r'\\Streaming-pc\d'
    
    try:
        available_files = os.listdir(video_folder)
    except Exception as e:
        logging.error(f"Error accessing the directory: {e}")
        return None

    logging.debug(f"Available files: {available_files}")


    for file in available_files:
        file_path = os.path.join(video_folder, file)
        if os.path.isfile(file_path) and file.endswith(".mp4"):
            created_date_str = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).date().strftime("%Y-%m-%d")
            created_date = datetime.datetime.strptime(created_date_str, "%Y-%m-%d").date()
            logging.debug(f"Checking file: {file}, Created date: {created_date}")
            logging.debug(f"today: {today}")

            # Calculate the difference between the file's creation date and today's date
            delta = abs(created_date - today)

            # If this is the first valid file or its creation date is closer to today's date,
            # update the closest file and delta
            if closest_delta is None or delta < closest_delta:
                closest_file = file_path
                closest_delta = delta

    if closest_file:
        logging.debug(f"Found closest video file: {closest_file}")
        return closest_file
    else:
        logging.error("No video file found.")
        return None

def uploadVimeo(video):
  client = vimeo.VimeoClient(
      token=os.getenv('VIMEO_TOKEN'),
      key=os.getenv("VIMEO_KEY"),
      secret=os.getenv("VIMEO_SECRET"),
    )
  logging.info("Starting uploadVimeo")
  post = getPost(f"{os.getenv('WP_API_URL')}posts?categories=48&per_page=1")
  logging.debug(f"Post: {post}")
  if post is None:
      logging.error("Failed to retrieve post from WordPress API")
      return None

  # Get the upload name
  upload_name = getName(post)
  if upload_name is None:
      logging.error("Failed to get upload name from getName.")
      return None
  
  logging.info(f"Starting {video} upload")
  tags = ["northcountrychapel", "ncc", "biblestudy"]
  regex = r'\b(?:[1-3]?\s?[a-zA-Z]+\s?[A-Za-z]*)\b'
  book_name = re.search(upload_name, regex)
  book_name_str = book_name.group(0) if book_name else "Unknown"

  video = getUploadVideo()

  try:
    uri = client.upload(video, data={
      'name': upload_name,
      'description': f'Join us as we study through the book of {book_name_str}',
      'privacy': {
          'view': 'nobody'  # prod = anybody
      },
        'content-rating': 'safe',
        "license": "by-nc-sa",
        "tags": tags,
    })
    logging.info(f"Finished upload. Video uri is {uri}")
    return uri
  except Exception as e:
    logging.error(f"An error occurred during the upload: {str(e)}")
    return None

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
      logging.info('Your video is still uploading. Next check in 5 minutes')
      time.sleep(300)
      return False
    else:
      logging.info('Your video encountered an error during uploading.')
      #TODO: report error
      break
  logging.info(f"Finished upload check. The uri is: {uri}")  
  return uri  

def getVideoInfo(uri):
  client = vimeo.VimeoClient(
      token=os.getenv('VIMEO_TOKEN'),
      key=os.getenv("VIMEO_KEY"),
      secret=os.getenv("VIMEO_SECRET"),
    )
  logging.info("Beginning getVideoInfo")
  try:
    video_info = client.get(f"https://api.vimeo.com{uri}").json()
    if video_info:
      logging.debug(video_info)
      logging.info("Returning video_info")
      return video_info
    else:
      logging.error("No video found")
  except Exception as e:
        logging.error(f"Failed to retrieve video info: {e}")


