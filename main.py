import shutil
from pathlib import Path

import uvicorn as uvicorn
from DECIMER import predict_SMILES
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

ALLOWED_FILE_TYPES = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG']

filestore = f"{Path(__file__).parents[0]}/'filestore"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/process_image")
def process_image(image: UploadFile = File(...), osr_type: str = 'decimer'):
    if not Path(image.filename).suffix in ALLOWED_FILE_TYPES:
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

