import os
from PIL import Image
import numpy as np


BACKGROUND_FILEPATH = os.path.join("Siamese-Network","Ommniglot_dataset", "images_background")
EVALUATION_FILEPATH = os.path.join("Ommniglot_dataset", "images_evaluation")

alphabet_dict = {}
print(BACKGROUND_FILEPATH)
for index, alphabet in enumerate(os.listdir(BACKGROUND_FILEPATH)):
    print(alphabet)