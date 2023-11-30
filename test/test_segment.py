from pathlib import Path

import requests

url = 'http://0.0.0.0:8080/segment_images_from_file'

data = {'paper_id': 'test_paper', 'filename': 'select_panel.png', 'osr_type': 'decimer'}
r = requests.post(url, json=data)
print(r.text)

"""
{"status":"success",
"filepaths":["select_panel_decimer_segmented_images/0.png","select_panel_decimer_segmented_images/1.png","select_panel_decimer_segmented_images/2.png","select_panel_decimer_segmented_images/3.png","select_panel_decimer_segmented_images/4.png","select_panel_decimer_segmented_images/5.png","select_panel_decimer_segmented_images/6.png","select_panel_decimer_segmented_images/7.png","select_panel_decimer_segmented_images/8.png","select_panel_decimer_segmented_images/9.png","select_panel_decimer_segmented_images/10.png","select_panel_decimer_segmented_images/11.png","select_panel_decimer_segmented_images/12.png","select_panel_decimer_segmented_images/13.png","select_panel_decimer_segmented_images/14.png","select_panel_decimer_segmented_images/15.png","select_panel_decimer_segmented_images/16.png","select_panel_decimer_segmented_images/17.png"],
"smis":["CCCCC(=O)C","CCOC(=O)CCC(=O)C","C1CCC(=O)C1","C1CCC(=O)CC1","C1C=CC(=O)CC1","C1C=CC(=CC1)C=O","CC(=O)CCC1=CCCC=C1","CC1=CC=C(C=C1)CC(=O)C","C1=CC=C2C(=C1)CCC2=O","CC[NH]","CC(C)[NH2]","CCCCN","C#CCN","C1CC1N","C#CCNC","C1C=CC(=CC1)N","C1C=CC(=CC1)CN","C1C=CC(=CC1)[C@@H]2C[C@H]2N"]}
"""