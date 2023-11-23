from pathlib import Path

import requests

url = 'http://0.0.0.0:8080/process_image'

# this dir
current_dur = str(Path(__file__).parents[0])
filepath = f"{current_dur}/test2.png"

files = {'image': open(filepath, 'rb')}

r = requests.post(url, files=files)

print(r.text)