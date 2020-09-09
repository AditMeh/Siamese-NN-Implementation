import os
from PIL import Image
import numpy as np

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


def generate_pairs(alphabet_name, index_of_character, index_of_image):
    current_character = train_dict[alphabet_name]["characters"][index_of_character]
    current_image = train_dict[alphabet_name][current_character][index_of_image]
    anchor = os.path.join(alphabet_name, current_character, current_image)
    print(anchor)

    numberOfCharacters = len(train_dict[alphabet_name]["characters"])
    for char_index in range(index_of_character, numberOfCharacters):
        if index_of_image != 0 and index_of_character == char_index:
            for image in range(index_of_image + 1, 20):
                character = train_dict[alphabet_name]["characters"][char_index]
                filepath = train_dict[alphabet_name][character][image]
                print(os.path.join(character, filepath))
        else:
            for image in range(0, 20):
                character = train_dict[alphabet_name]["characters"][char_index]
                filepath = train_dict[alphabet_name][character][image]
                print(os.path.join(character, filepath))


for alphabet in os.listdir(BACKGROUND_FILEPATH):
    for index_character, character_path in enumerate(os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet))):
        for index_image, image in enumerate(os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, character_path))):
            generate_pairs(alphabet, index_character, index_image)
    break
