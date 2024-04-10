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
            random_number = random.uniform(0.5, 1)
            weight = round(random_number, 1) * 0.7
            weightList.append(round(weight, 2))
        return weightList

    def train(self, learning_rate=0.1, epochs=1000):
        # Loop through each epoch
        for epoch in range(epochs):
            # Loop through each language vector
            for lang_name in self.language_vectors:
                lang_vector = self.language_vectors[lang_name]
                lang_index = self.get_lang_index(lang_name)

                # Calculate the net value for each weight vector
                net_values = []
                for weights in self.weights:
                    net_value = 0
                    for i in range(len(weights)):
                        net_value += lang_vector[i] * weights[i]
                    net_values.append(net_value)


                # Update the weights
                for i in range(len(self.weights)):
                    # If the weight vector corresponds to the current language vector
                    if i == lang_index:
                        # Update the weights to move closer to 1
                        self.update_weights(i, learning_rate, direction='increase')
                    else:
                        # Update the weights to move closer to 0
                        self.update_weights(i, learning_rate, direction='decrease')

    def get_lang_index(self, lang_name):
        # Get the index of the language vector
        for index in range(len(self.languages)):
            if self.languages[index] == lang_name:
                return index

    def update_weights(self, index, learning_rate, direction='increase'):
        # Update the weights based on the specified direction
        for j in range(len(self.weights[index])):
            if direction == 'increase':
                # Move the weight closer to 1
                self.weights[index][j] += learning_rate * (1 - self.weights[index][j])
            elif direction == 'decrease':
                # Move the weight closer to 0
                self.weights[index][j] -= learning_rate * self.weights[index][j]

    def load_data(self, data_dir):
        for lang_folder in os.listdir(data_dir):
            self.languages.append(lang_folder)
            lang_path = os.path.join(data_dir, lang_folder)
            lang_vector = [0] * 128  # ASCII characters
            total_files = 0
            for file_name in os.listdir(lang_path):
                total_files += 1
                with open(os.path.join(lang_path, file_name), 'r', encoding='utf-8') as file:
                    text = file.read()
                    for char in text:
                        if ord(char) < 128:  # considering only ASCII characters
                            lang_vector[ord(char)] += 1/9
            self.language_vectors[lang_folder] = [freq / total_files for freq in lang_vector]

    def classify(self, text):
        input_vector = [0] * 128  # Initialize input vector for ASCII characters
        for char in text:
            if ord(char) < 128:
                input_vector[ord(char)] += 1

        net = []
        for weights in self.weights:
            net_value = 0
            for i in range(len(input_vector)):
                net_value += input_vector[i] * weights[i]
            net.append(net_value)

        max_index = net.index(max(net))  # Find the index of the maximum net value
        return self.languages[max_index]  # Return the language corresponding to the maximum net value


if __name__ == '__main__':
    classifier = Neuron()
    classifier.load_data("C:\\Users\\demir\\Documents\\git\\nai-projects\\project3\\languages")
    num_languages = len(classifier.languages)
    classifier.weights = [classifier.initalize_weights(128) for _ in range(num_languages)]
    classifier.train()
    while True:
        text = input("Enter text to classify: ")
        if text.lower() == "exit":
            break
        language = classifier.classify(text)
        print("Predicted language:", language)
