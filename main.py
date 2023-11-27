import json
import shutil
from pathlib import Path

import uvicorn as uvicorn
from DECIMER import predict_SMILES
from fastapi import FastAPI, UploadFile, File
from decimer_segmentation import segment_chemical_structures_from_file

app = FastAPI()

filestore = f"{Path(__file__).parents[0]}/'filestore"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/process_image")
def process_image(image: UploadFile = File(...), osr_type: str = 'decimer'):
    file_types = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG']

    if not Path(image.filename).suffix in file_types:
        return {'status': 'error',
                'msg': 'file type not allowed'}

    # save image to work on it
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # check it saved ok
    if not Path(image.filename).exists():
        return {'status': 'error',
                'msg': 'file does not exist'}

    # run osr
    if osr_type == 'decimer':
        smi = predict_SMILES(image.filename)
    else:
        return {'status': 'error',
                'msg': 'osr type not recognised'}

    # remove image
    Path(image.filename).unlink()

    return {'status': 'success',
            'smi': smi}

@app.post("/segment_images_from_file")
def segment_images_from_file(image: UploadFile = File(...)):
    file_types = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG', '.pdf', '.PDF']

    if not Path(image.filename).suffix in file_types:
        return {'status': 'error',
                'msg': 'file type not allowed'}

    # save image to work on it
    print(image.filename)
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # check it saved ok
    if not Path(image.filename).exists():
        return {'status': 'error',
                'msg': 'file does not exist'}

    segments = segment_chemical_structures_from_file(image.filename, expand=True)
    segments_json = json.dumps([s.tolist() for s in segments])

    # remove image
    Path(image.filename).unlink()

    return {'status': 'success',
            'segments': segments_json}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

