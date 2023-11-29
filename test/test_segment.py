from pathlib import Path

import requests

url = 'http://0.0.0.0:8080/segment_images_from_file'

data = {'paper_id': 'test_paper', 'filename': 'select_panel.png', 'osr_type': 'decimer'}
r = requests.post(url, json=data)
print(r.text)

#data = {'paper_id': 'test_paper', 'filename': 'main.pdf', 'osr_type': 'decimer'}
#r = requests.post(url, json=data)
#print(r.text)