import random


def initializeThreshold():
    random_number = random.uniform(0.1, 1)
    threshold = round(random_number, 1) * 0.5
    return threshold

def initializeWeights(size):
    weightList = []
    for i in range(size-1):
        random_number = random.uniform(0.1, 1)
        weight = round(random_number, 1) * 0.5
        weightList.append(weight)
    return weightList

def getContentOfFile(filePath):
    with open(filePath, 'r') as file:
        content = file.readlines()
    return content

"""dot product : testfile each * weights each,
 in the end answer is bigger than threshold y is 1 otherwise 0."""
""" delta rule = weights old + ( last element of the line + y )
 * learning rate * rest elements of file"""
def dotProduct(testFileLine, weightList,threshold):
    calculations = []
    for i,y in range(len(testFileLine)-1):
        testFile = testFileLine[i]


def main_method():
    trainingFilePath = input("enter training file path = ")
    testFilePath = input("enter test file path = ")
    learningRate = float(input("enter learning rate = "))
    epochs = int(input("enter number of epochs = "))

main_method()



