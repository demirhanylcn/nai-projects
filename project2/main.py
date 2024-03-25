import random


def initializeThreshold():
    random_number = random.uniform(0.1, 1)
    threshold = round(random_number, 1) * 0.5
    return threshold

def initializeWeights(size):
    weights = []
    for i in range(size-1):
        random_number = random.uniform(0.1, 1)
        weight = round(random_number, 1) * 0.5
        weights.append(weight)

"""dot product : testfile each * weights each,
 in the end answer is bigger than threshold y is 1 otherwise 0."""
""" delta rule = weights old + ( last element of the line + y )
 * learning rate * rest elements of file"""
def dotProduct():



def main_method():
    trainingFilePath = input("enter training file path = ")
    testFilePath = input("enter test file path = ")
    learningRate = float(input("enter learning rate = "))
    epochs = int(input("enter number of epochs = "))

main_method()



