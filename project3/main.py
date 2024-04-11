import os
import random


def initialize_weights(size):
    weight_list = []
    for _ in range(size):
        random_number = random.uniform(0.2, 0.5)
        weight = random_number * 0.7
        weight_list.append(weight)
    return weight_list


def train(weights, languages, language_vectors, learning_rate, epochs):
    for _ in range(epochs):
        for lang_name in languages:
            lang_index = languages.index(lang_name)
            for i in range(len(weights)):
                input_vector = language_vectors[lang_name]
                is_correct_language = (i == lang_index)
                update_weights(weights, i, learning_rate, input_vector, is_correct_language)


def update_weights(weights, index, learning_rate, input_vector, is_correct_language):
    for j in range(len(weights[index])):
        if is_correct_language:
            weights[index][j] += learning_rate * input_vector[j]
        else:
            weights[index][j] -= learning_rate * input_vector[j]


def find_chars(data_dir):
    languages = []
    language_vectors = {}
    for lang_folder in os.listdir(data_dir):
        languages.append(lang_folder)
        lang_path = os.path.join(data_dir, lang_folder)
        lang_vector = [0] * 128
        total_files = 0
        for file_name in os.listdir(lang_path):
            total_files += 1
            with open(os.path.join(lang_path, file_name), 'r', encoding='utf-8') as file:
                text = file.read()
                for char in text:
                    if ord(char) < 128:
                        lang_vector[ord(char)] += 1
        language_vectors[lang_folder] = [freq / 128 for freq in lang_vector]
    return languages, language_vectors


def prediction(text, weights, languages):
    input_vector = [0] * 128
    for char in text:
        if ord(char) < 128:
            input_vector[ord(char)] += 1

    net = []
    for weight in weights:
        net_value = 0
        for i in range(len(input_vector)):
            net_value += input_vector[i] * weight[i]
        net.append(net_value)
    max_index = net.index(max(net))
    return languages[max_index]


if __name__ == '__main__':
    data_dir = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project3\\languages"
    languages, language_vectors = find_chars(data_dir)
    language_count = len(languages)
    weights = [initialize_weights(128) for _ in range(language_count)]
    epoch = int(input("Enter number of epochs: "))
    learning_rate = float(input("Enter learning rate: "))
    train(weights, languages, language_vectors, learning_rate, epoch)
    while True:
        text = input("Enter the sentence: ")
        language = prediction(text, weights, languages)
        print("Predicted language:", language)
