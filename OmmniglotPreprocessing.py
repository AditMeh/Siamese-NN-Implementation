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
    anchor = Image.open(os.path.join(BACKGROUND_FILEPATH, alphabet_name, current_character, current_image))
    anchor = np.asarray(anchor).astype(np.float32)
    print(current_image)
    output = [[], []]
    numberOfCharacters = len(train_dict[alphabet_name]["characters"])
    for char_index in range(index_of_character, numberOfCharacters):
        if index_of_image != 0 and index_of_character == char_index:
            for image in range(index_of_image + 1, 20):
                character = train_dict[alphabet_name]["characters"][char_index]
                filepath = train_dict[alphabet_name][character][image]
                curr_image = Image.open(os.path.join(BACKGROUND_FILEPATH, alphabet_name, character, filepath))
                curr_image = np.asarray(curr_image).astype(np.float32)

                output[0].append([anchor, curr_image])

        else:
            for image in range(0, 20):
                character = train_dict[alphabet_name]["characters"][char_index]
                filepath = train_dict[alphabet_name][character][image]
                curr_image = Image.open(os.path.join(BACKGROUND_FILEPATH, alphabet_name, character, filepath))
                curr_image = np.asarray(curr_image).astype(np.float32)

                output[1].append([anchor, curr_image])

    return output


for alphabet in os.listdir(BACKGROUND_FILEPATH):
    bins = [[], []]
    print(alphabet)
    for index_character, character_path in enumerate(os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet))):
        for index_image, image in enumerate(os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, character_path))):
            result = generate_pairs(alphabet, index_character, index_image)
            bins[0].extend(result[0])
            bins[1].extend(result[1])

x = np.asarray(bins[0])
y = np.asarray(bins[1])
print(x.shape)
print(y.shape)
