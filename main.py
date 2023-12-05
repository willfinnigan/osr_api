from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from PIL import Image

from models import decimer_model, molscribe_model

app = FastAPI()

filestore = f"{Path(__file__).parents[0]}/filestore"

@app.get("/")
async def root():
    return {"message": "Hello World"}

class ImageData(BaseModel):
    filename: str
    paper_id: str
    osr_type: str = 'decimer'

@app.post("/process_image")
async def process_image(request: Request, image_data: ImageData):
    file_types = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG']

    filepath = f"{filestore}/{image_data.paper_id}/molecule_images/{image_data.filename}"

    if not Path(filepath).suffix in file_types:
        response = {'status': 'error',
                'msg': 'file type not allowed'}
        print(response)
        return response

    # check file exists
    if not Path(filepath).exists():
        response = {'status': 'error',
                'msg': 'file does not exist'}
        print(response)
        return response

    # run osr
    if image_data.osr_type == 'decimer':
        smi = decimer_model.predict(filepath)
        response = {'status': 'success',
                    'smi': smi}
    elif image_data.osr_type == 'molscribe':
        output = molscribe_model.predict(filepath)
        smi = output['smiles']
        response = {'status': 'success',
                    'smi': smi}
    else:
        response = {'status': 'error',
                'msg': 'osr type not recognised'}

    print(response)
    return response

@app.post("/segment_images_from_file")
async def decimer_segment(request: Request, image_data: ImageData):
    from decimer_segmentation import segment_chemical_structures_from_file
    file_types = ['.png', '.jpeg', '.PNG', '.JPEG', '.jpg', '.JPG', '.pdf', '.PDF']

    filepath = f"{filestore}/{image_data.paper_id}/molecule_images/{image_data.filename}"

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
            smi = decimer_model.predict(fullpath)
            smis.append(smi)
        elif image_data.osr_type == 'molscribe':
            output = molscribe_model.predict(filepath, return_atoms_bonds=True, return_confidence=False)
            smi = output['smiles']
            smis.append(smi)

    return {'status': 'success',
            'filepaths': saved_filepaths,
            'smis': smis}

if __name__ == "__main__":
    # set the PYSTOW_HOME environment variable to the path of the folder where you want to store the models
    # e.g. export PYSTOW_HOME=/home/user/models

    molscribe_model.molscribe_model_path = "/Users/willfinnigan/Documents/model/modal/MOLSCRIBE/swin_base_char_aux_1m.pth"
    filestore = f"/Users/willfinnigan/PycharmProjects/retrobiocat/retrobiocat_web/app/database_bps/curation/filestore"

    uvicorn.run(app, host="0.0.0.0", port=8080)