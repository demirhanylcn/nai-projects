import os
import random


class Neuron:
    def __init__(self):
        self.languages = []
        self.language_vectors = {}
        self.weights = []

    def initalize_weights(self, size):
        weightList = []
        for i in range(size):
            random_number = random.uniform(0.2, 0.5)
            weight = round(random_number, 1) * 0.7
            weightList.append(round(weight, 2))
        return weightList

    def train(self, learning_rate, epochs):
        for epoch in range(epochs):
            for lang_name in self.languages:
                lang_index = self.get_language_index(lang_name)
                for i in range(len(self.weights)):
                    input_vector = self.language_vectors[lang_name]
                    is_correct_language = (i == lang_index)
                    self.update_weights(i, learning_rate, input_vector, is_correct_language)

    def get_language_index(self, lang_name):

        for index in range(len(self.languages)):
            if self.languages[index] == lang_name:
                return index

    def update_weights(self, index, learning_rate, input_vector, is_correct_language):
        for j in range(len(self.weights[index])):
            if is_correct_language:
                self.weights[index][j] += learning_rate * input_vector[j]
            else:
                self.weights[index][j] -= learning_rate * input_vector[j]

    def find_chars(self, data_dir):
        for lang_folder in os.listdir(data_dir):
            self.languages.append(lang_folder)
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
            self.language_vectors[lang_folder] = [freq / 128 for freq in lang_vector]

    def prediction(self, text):
        input_vector = [0] * 128
        for char in text:
            if ord(char) < 128:
                input_vector[ord(char)] += 1

        net = []
        for weights in self.weights:
            net_value = 0
            for i in range(len(input_vector)):
                net_value += input_vector[i] * weights[i]
            net.append(net_value)
        print(net)
        max_index = net.index(max(net))
        return self.languages[max_index]


if __name__ == '__main__':
    neuron = Neuron()
    neuron.find_chars("C:\\Users\\demir\\Documents\\git\\nai-projects\\project3\\languages")
    language_count = len(neuron.languages)
    neuron.weights = [neuron.initalize_weights(128) for _ in range(language_count)]
    epoch = int(input("Enter number of epochs: "))
    learning_rate = float(input("Enter learning rate: "))
    neuron.train(learning_rate, epoch)
    while True:
        text = input("Enter the sentence: ")
        language = neuron.prediction(text)
        print("Predicted language:", language)
