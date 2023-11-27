from pathlib import Path

import requests

url = 'http://0.0.0.0:8080/segment_images_from_file'

# this dir
current_dur = str(Path(__file__).parents[0])
filepath = f"{current_dur}/panel.png"

files = {'image': open(filepath, 'rb')}

r = requests.post(url, files=files)

print(r.text)