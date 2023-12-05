import pystow
import torch
from molscribe import MolScribe


class MolScribeModel():

    def __init__(self, modal_path=None):
        self.model = None
        if modal_path is not None:
            self.molscribe_model_path = modal_path
        else:
            pystow_path = pystow.join('MOLSCRIBE')
            self.molscribe_model_path = f"{pystow_path}/swin_base_char_aux_1m.pth"

    def load_model(self):
        if self.model is None:
            self.model = MolScribe(self.molscribe_model_path, device=torch.device('cpu'))

    def predict(self, filepath):
        self.load_model()
        return self.model.predict_image_file(filepath, return_atoms_bonds=True, return_confidence=False)

molscribe_model = MolScribeModel()


class DECIMER_Model():

    def load_model(self):
        from DECIMER import predict_SMILES

    def predict(self, filepath):
        from DECIMER import predict_SMILES
        return predict_SMILES(filepath)

decimer_model = DECIMER_Model()

