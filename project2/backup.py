import random


def getContentFromSTREnding(filePath):
    type_map = {}
    with open(filePath, 'r') as file:
        for line in file:
            type_name = line.strip().split(',')[-1]
            if type_name not in type_map:
                type_map[type_name] = len(type_map)

    content = getContentOfFile(filePath)
    for i in range(len(content)):
        line = content[i]
        if line[-1] in type_map:
            label = type_map[line[-1]]
            line[-1] = str(label)
    return content


def initializeThreshold():
    random_number = random.uniform(0.5, 1)
    threshold = round(random_number, 1) * 0.7
    return threshold


def initializeWeights(size):
    weightList = []
    for i in range(size):
        random_number = random.uniform(0.5, 1)
        weight = round(random_number, 1) * 0.7
        weightList.append(round(weight,2))
    return weightList


def getContentOfFile(filePath):
    with open(str(filePath), 'r') as file:
        content = file.readlines()

    contentStripped = []
    for i in range(len(content)):
        line = content[i].strip("\n").split(",")
        contentStripped.append(line)

    random.shuffle(contentStripped)
    return contentStripped


"""dot product : testfile each * weights each,
 in the end answer is bigger than threshold y is 1 otherwise 0."""
""" delta rule = weights old + ( last element of the line + y )
 * learning rate * rest elements of file"""


def calculations(testFilePath, learningRate, epoch, isTxt):
    file = getContentOfFile(testFilePath)
    size = len(file[0])-1
    newWeights = initializeWeights(size)
    threshold = initializeThreshold()
    accuracies = []
    for eachEpoch in range(epoch):
        if (isTxt):
            testFile = getContentFromSTREnding(testFilePath)
        else:
            testFile = getContentOfFile(testFilePath)
        trueCount = 0
        for i in range(len(testFile)):
            line = testFile[i]
            d = int(line[len(line) - 1])
            print(line)
            print(newWeights)
            print(dotProduct(line,newWeights))
            print(threshold)
            if dotProduct(line, newWeights) > float(threshold):
                y = 1
            else:
                y = 0
            print(y)
            if d == y:
                trueCount += 1
            else:
                newWeights = deltaRule(newWeights, y, learningRate, line)

        accuracies.append((trueCount / len(testFile)) * 100)
    return accuracies


def dotProduct(line, weightList):
    sum = 0
    for i in range(len(weightList)):
        sum += float(line[i]) * weightList[i]
    return sum


def deltaRule(weightList, y, learningRate, line):
    newWeights = []
    rightCalculation = []
    d = int(line[-1])
    dMinusY = y - d
    dMinusYTimesLearningRate = dMinusY * learningRate
    for i in range(len(weightList)):
        rightCalculation.append(float(line[i]) * dMinusYTimesLearningRate)
    for j in range(len(weightList)):
        newWeights.append(round(rightCalculation[j] + weightList[j]))
    return newWeights


def main_method():
    trainingFilePath = str(input("enter the filepath = "))
    isTxt = bool(input("is the file label string? [0] False [1] True = "))
    learningRate = float(input("enter learning rate = "))
    epochs = int(input("enter number of epochs = "))
    answer = calculations(trainingFilePath, learningRate, epochs, isTxt)
    print(answer)


main_method()
