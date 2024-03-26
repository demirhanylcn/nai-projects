import random


def initializeThreshold():
    random_number = random.uniform(0.1, 0.5)
    threshold = round(random_number, 1) * 0.5
    return threshold


def initializeWeights(size):
    weightList = []
    for i in range(size - 1):
        random_number = random.uniform(0.1, 1)
        weight = round(random_number, 1) * 0.5
        weightList.append(weight)
    return weightList


def getContentOfFile(filePath):
    with open(str(filePath), 'r') as file:
        content = file.readlines()

    random.shuffle(content)
    print(content)
    return content


"""dot product : testfile each * weights each,
 in the end answer is bigger than threshold y is 1 otherwise 0."""
""" delta rule = weights old + ( last element of the line + y )
 * learning rate * rest elements of file"""


def calculations(testFilePath, weightList, threshold, learningRate, epoch):
    newWeights = weightList
    accuracies = []
    for eachEpoch in range(0, epoch):
        testFile = getContentOfFile(testFilePath)
        trueCount = 0
        for i in range(len(testFile)):
            line = testFile[i]
            for t in range(len(line) - 1):
                if dotProduct(line, weightList) > threshold:
                    y = 1
                    trueCount += 1
                else:
                    y = 0
                if y == 0:
                    newWeights = deltaRule(newWeights, y, learningRate, line)
                    print(newWeights)
        accuracies.append(trueCount / len(testFile))

    return accuracies


def dotProduct(line, weightList):
    sum = 0
    for i in range(len(line) - 1):
        sum += float(line[i]) * weightList[i]
        return sum


def deltaRule(weightList, y, learningRate, line):
    newWeights = []
    rightCalculation = []
    dMinusY = float(line.strip().split(",")[len(line) - 1]) - float(y)
    dMinusYTimesLearningRate = float(dMinusY) * float(learningRate)
    for i in range(len(line) - 1):
        rightCalculation.append(line[i] * dMinusYTimesLearningRate)
    for y in range(len(weightList)):
        newWeights.append(rightCalculation[y] + weightList[y])
    return newWeights


def main_method():
    trainingFilePath = input("enter training file path = ")
    learningRate = float(input("enter learning rate = "))
    epochs = int(input("enter number of epochs = "))
    answer = calculations(trainingFilePath, initializeWeights(2), initializeThreshold(), learningRate, epochs)
    print(answer)


""" testFilePath = input("enter test file path = ")"""
main_method()
