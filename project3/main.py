import os
import random


class Perceptron:
    def __init__(self,training_file_path,test_file_path):
        self.weights = []
        self.learning_rate = 0
        self.threshold = 0
        self.epoch = 0
        self.accuracy = 0
        self.training_file_path = training_file_path
        self.testing_file_path = test_file_path

    def initializeThreshold(self):
        random_number = random.uniform(0.5, 1)
        self.threshold = round(random_number, 1) * 0.7

    def deltaRule(self,d, y, line):
        newWeights = []
        for i in range(len(self.weights)):
            newWeights.append(self.weights[i] + (self.learning_rate * (d - y) * float(line[i])))
        return newWeights

    def initialize_weights(self):
        for _ in range(len(self.weights)):
            random_number = random.uniform(0.2, 0.5)
            weight = random_number * 0.7
            self.weights.append(weight)

    def dotProduct(self, vector):
        sum = 0
        for i in range(len(self.weights)):
            sum += float(vector[i]) * self.weights[i]
        return sum
    def get_inputs(self):
        self.epoch = int(input("Enter number of epochs: "))
        self.learning_rate = float(input("Enter learning rate: "))
        self.initializeThreshold()
        self.initialize_weights()

    def read_content(self,file_path):
        """"""



def train_n_test(self):

        training_set = self.read_content('')



"""def train():


def test():


def dot_product():


def proportions():


def predict_language():





if __name__ == '__main__':
    test_files = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project3\\test"
    train_files = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project3\\train"
    language_count = len(os.listdir(test_files))
    epochs, learning_rate = get_user_inputs()
    while True:
        text = input("Enter the sentence: ")
        language = predict_language()
        print("Predicted language:", language)
"""

if __name__ == '__main__':
    """"""