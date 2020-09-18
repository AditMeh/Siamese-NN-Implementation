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


def random_sampler_with_exclusion(sample_size, exclusion, list_to_sample):
    remove_index = list_to_sample.index(exclusion)
    del list_to_sample[remove_index]

    sample = rand.sample(list_to_sample, sample_size)
    sample.append(exclusion)
    return sample


def generate_pairs():
    bins_same = []
    bins_different = []
    for alphabet in os.listdir(BACKGROUND_FILEPATH):
        for character in os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet)):
            sampled_characters = random_sampler_with_exclusion(5, character,
                                                               os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet)))
            print(os.path.join(alphabet, character))
            for iter_character in sampled_characters:
                if iter_character == character:
                    sampled_images = rand.sample(os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, character)), 18)
                    for sampled_images_index in range(len(sampled_images) - 1):
                        image_1 = np.array(io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, character,
                                                                  sampled_images[sampled_images_index])))

                        image_2 = np.array(io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, character,
                                                                  sampled_images[sampled_images_index + 1])))
                        bins_same.append([image_1, image_2])
                else:
                    sampled_images_char = rand.sample(os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, character))
                                                      , 5)
                    sampled_images_iter_char = rand.sample(
                        os.listdir(os.path.join(BACKGROUND_FILEPATH, alphabet, iter_character))
                        , 5)

                    for sampled_images_index in range(len(sampled_images_char) - 1):
                        image_1 = np.asarray(io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, character,
                                                                    sampled_images_char[sampled_images_index])))

                        image_2 = np.asarray(io.imread(os.path.join(BACKGROUND_FILEPATH, alphabet, iter_character,
                                                                    sampled_images_iter_char[
                                                                        sampled_images_index + 1])))
                        bins_different.append([image_1, image_2])

    return bins_same, bins_different


bins_same, bins_different = generate_pairs()
bins_same = np.asarray(bins_same).astype(np.float32)
bins_different = np.asarray(bins_different).astype(np.float32)



"""
pickle_out = open("dataset.pickle", "wb")
pickle.dump(answer, pickle_out)
pickle_out.close()
"""
