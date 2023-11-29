import json
import shutil
from pathlib import Path

import uvicorn as uvicorn
from DECIMER import predict_SMILES
from PIL import Image
from fastapi import FastAPI, APIRouter, Request
from decimer_segmentation import segment_chemical_structures_from_file
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

filestore = f"{Path(__file__).parents[0]}/filestore"

class ImageData(BaseModel):
    filename: str
    paper_id: str
    osr_type: str = 'decimer'

@router.post("/process_image")
async def process_image(request: Request, image_data: ImageData):
    file_types = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG']

    filepath = f"{filestore}/{image_data.paper_id}/{image_data.filename}"

    if not Path(filepath).suffix in file_types:
        return {'status': 'error',
                'msg': 'file type not allowed'}

    # check file exists
    if not Path(filepath).exists():
        return {'status': 'error',
                'msg': 'file does not exist'}

    # run osr
    if image_data.osr_type == 'decimer':
        smi = predict_SMILES(filepath)
    else:
        return {'status': 'error',
                'msg': 'osr type not recognised'}

    return {'status': 'success',
            'smi': smi}

@router.post("/segment_images_from_file")
async def decimer_segment(request: Request, image_data: ImageData):
    file_types = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG', '.pdf', '.PDF']

    filepath = f"{filestore}/{image_data.paper_id}/{image_data.filename}"

    if not Path(filepath).suffix in file_types:
        return {'status': 'error',
                'msg': 'file type not allowed'}

    # check file exists
    if not Path(filepath).exists():
        return {'status': 'error',
                'msg': 'file does not exist'}

    segments = segment_chemical_structures_from_file(filepath, expand=True)

    # make folder to save segmented images to
    filename_no_suffix = Path(image_data.filename).stem
    new_folder = f"{filename_no_suffix}_decimer_segmented_images"
    save_folder = f"{filestore}/{image_data.paper_id}/{new_folder}"
    Path(save_folder).mkdir(parents=True, exist_ok=True)

    # save segmented images
    saved_filepaths = []
    smis = []
    for i, segment in enumerate(segments):
        fullpath = f"{filestore}/{image_data.paper_id}/{new_folder}/{i}.png"
        shortpath = f"{new_folder}/{i}.png"

        img = Image.fromarray(segment)
        img.save(fullpath)
        saved_filepaths.append(shortpath)

        if image_data.osr_type == 'decimer':
            smi = predict_SMILES(fullpath)
            smis.append(smi)

    return {'status': 'success',
            'filepaths': saved_filepaths,
            'smis': smis}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

