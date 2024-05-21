import vimeo
import os
import get_wp_title
import re
from dotenv import load_dotenv

load_dotenv()

client = vimeo.VimeoClient(
    token=os.getenv('VIMEO_TOKEN'),
    key=os.getenv("VIMEO_KEY"),
    secret=os.getenv("VIMEO_SECRET"),
  )


upload_name = get_wp_title.getName(os.getenv("WP_API_URL"))

desktop = os.path.expanduser("~/Desktop")
file_name = desktop + "/thurber.eric.mp4"
tags = ["northcountrychapel", "ncc", "biblestudy"]
regex = r'\b(?:[1-3]?\s?[a-zA-Z]+\s?[A-Za-z]*)\b'
book_name = re.search(upload_name, regex)

uri = client.upload(file_name, data={
  'name': upload_name,
  'description': 'Join us as we study through the book of '+ str(book_name),
  'privacy': {
    'view': 'nobody' # prod = anybody
  },
  'content-rating': 'safe',
  "tags": tags, 
  })

print('Your video URI is: %s' % (uri))


# response = client.get(uri + '?fields=transcode.status').json()
# if response['transcode']['status'] == 'complete':
#   print('Your video finished transcoding.')
# elif response['transcode']['status'] == 'in_progress':
#   print('Your video is still transcoding.')
# else:
#   print('Your video encountered an error during transcoding.')