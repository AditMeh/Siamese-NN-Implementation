import os
from skimage import io
import numpy as np
import random as rand
import pickle

BACKGROUND_FILEPATH = os.path.join("Ommniglot_dataset", "images_background")
EVALUATION_FILEPATH = os.path.join("Ommniglot_dataset", "images_evaluation")

bins = []


def initialize_dictionary():
    train_dict = {}
    for alphabet in os.listdir(BACKGROUND_FILEPATH):
        train_dict[alphabet] = {}
        character_array = []

        for character_path in os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet)):
            image_array = []
            character_array.append(character_path)

            for image in os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, character_path)):
                image_array.append(image)

            train_dict[alphabet][character_path] = image_array
        train_dict[alphabet]["characters"] = character_array

    return train_dict


train_dict = initialize_dictionary()

classes = train_dict.keys()
classes_dict = {value: i for i, value in enumerate(os.listdir(BACKGROUND_FILEPATH))}

print(classes_dict)


def generate_pairs():
    bins = []
    for alphabet in os.listdir(BACKGROUND_FILEPATH):
        output = [[], []]
        for character in os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet)):
            for image in os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, character)):

                anchor = io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, character, image))
                anchor = np.asarray(anchor)

                characters = rand.sample(train_dict[alphabet]["characters"], 4)

                print(os.path.join(alphabet, character, image))
                characters.append(character)

                for item in characters:
                    if item == character:
                        iter_images = [k for k in train_dict[alphabet][item]]
                        for image_sample in iter_images:
                            curr_image = io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, item, image_sample))
                            curr_image = np.asarray(curr_image)
                            output[0].append([anchor, curr_image])

                    else:
                        iter_images = rand.sample(train_dict[alphabet][item], 5)
                        for image_sample in iter_images:
                            curr_image = io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, item, image_sample))
                            curr_image = np.asarray(curr_image)
                            output[1].append([anchor, curr_image])
        bins.append(output)

    return bins


answer = np.asarray(generate_pairs())


pickle_out = open("dataset.pickle", "wb")
pickle.dump(answer, pickle_out)
pickle_out.close()
