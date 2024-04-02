import random
import sys


def is_integer(word):
    try:
        int(word)
        return True
    except ValueError:
        return False


def is_file_containing_integers(filePath):
    with open(filePath, 'r') as file:
        for line in file:
            if not is_integer(line.strip("\n".split(",")[-1])):
                return False
    return True


def ValueLabels(filePath):
    type_map = {}
    with open(filePath, 'r') as file:
        for line in file:
            type_name = line.strip().split(',')[-1]
            if type_name not in type_map:
                type_map[type_name] = len(type_map)

    return type_map


def check_length_of_file(filePath):
    with open(filePath, 'r') as file:
        for line in file:
            return len(line.strip("\n").split(","))


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
        weightList.append(round(weight, 2))
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


def calculations(training_file_path, test_file_path, learningRate, epoch):
    size = check_length_of_file(training_file_path)
    newWeights = initializeWeights(size-1)
    threshold = initializeThreshold()
    accuracies = []

    if is_file_containing_integers(training_file_path):
        is_string = False
    else:
        is_string = True

    for eachEpoch in range(0, epoch):
        if is_string:
            training_file = getContentFromSTREnding(training_file_path)
            test_file = getContentFromSTREnding(test_file_path)
        else:
            training_file = getContentOfFile(training_file_path)
            test_file = getContentOfFile(test_file_path)
        trueCount = 0
        for i in range(len(training_file)):
            line = training_file[i]
            training_d = int(line[len(line) - 1])
            if dotProduct(line, newWeights) > float(threshold):
                training_y = 1
            else:
                training_y = 0
            if training_d == training_y:
                continue
            else:
                newWeights = deltaRule(newWeights, training_y, learningRate, line)
        for j in range(len(test_file)):
            line = training_file[j]
            test_d = int(line[len(line) - 1])
            if dotProduct(line, newWeights) > float(threshold):
                test_y = 1
            else:
                test_y = 0
            if test_d == test_y:
                trueCount += 1
        accuracies.append((trueCount / len(test_file)) * 100)
    answers = accuracies.copy()
    answers.append(newWeights)
    answers.append(threshold)
    return answers


def dotProduct(line, weightList):
    sum = 0
    for i in range(len(weightList)):
        sum += float(line[i]) * weightList[i]
    return sum


def deltaRule(weightList, y, learningRate, line):
    newWeights = []
    for i in range(len(weightList)):
        newWeights.append(round(weightList[i] + (learningRate * (int(line[-1]) - y) * float(line[i])), 2))
    return newWeights


def checkNewObservation(observation, last_answer, test_file_path):
    if is_file_containing_integers(test_file_path):
        is_string = False
    else:
        is_string = True

    observation = observation.strip("\n").split(",")
    if is_string:
        labels = ValueLabels(test_file_path)
        if observation[-1] not in labels:
            print("this label doesnt exists in the file.")
        else:
            float_observation = [float(each) for each in observation[:-1]]
            weights = last_answer[-2]
            threshold = last_answer[-1]
            observation_d = labels[observation[-1]]
            if dotProduct(float_observation, weights) > float(threshold):
                y = 1
            else:
                y = 0
            if observation_d == y:
                return True
            else:
                return False
    else:
        int_observation = [int(each) for each in observation]
        weights = last_answer[-2]
        threshold = last_answer[-1]
        observation_d = int_observation[-1]
        if dotProduct(int_observation, weights) > float(threshold):
            y = 1
        else:
            y = 0
        if observation_d == y:
            return True
        else:
            return False


def main_method():

    # training_file_path = input("Enter the training file path: ")
    # test_file_path = input("Enter the test file path: ")

    #INTEGERS
    #training_file_path = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project2\\train.txt"
    #test_file_path = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project2\\test.txt"

    #VERSI-ETC.
    training_file_path = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project2\\txtWithLabel\\training.txt"
    test_file_path = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project2\\txtWithLabel\\test.txt"
    learningRate = float(input("Enter the learning rate: "))
    epochs = int(input("Enter the number of epochs: "))
    answer = calculations(training_file_path, test_file_path, learningRate, epochs)
    for i in range(len(answer) - 2):
        print(f"accuracy[{i}] {answer[i]}")

    while (True):
        input_of_user = int(input("[0] Enter new observation.\n"
                                  "[1] Exit the program.\n"
                                  "Your input = "))
        if input_of_user < 0 or input_of_user > 1:
            print("Invalid input. Try again.")
        elif input_of_user == 0:
            new_observation = str(input("Enter the new observation: "))
            print(checkNewObservation(new_observation, answer, test_file_path))

        else:
            sys.exit()


main_method()
