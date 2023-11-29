import requests

url = 'http://0.0.0.0:8080/process_image'
data = {'paper_id': 'test_paper', 'filename': 'test2.png', 'osr_type': 'decimer'}
r = requests.post(url, json=data)

print(r.text)