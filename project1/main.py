"""Write an implementation of the K nearest neighbors (kNN) algorithm.
The square of the Euclidean distance should be used to calculate the distance between observations.
After starting the program, the user provides the path to the training file.
Then, the user (in the console) enters the number K, which denotes the number of nearest neighbors.
The program, running in a loop, allows you to choose one of 3 options:
a) classification of all observations from the test set given in a separate file -
the program allows you to provide the path to the file with the test set, assigns a
 label and prints the answer for each observation and then provides the accuracy for the entire set
b) classification of the observation given by the user in the console - the program
 loads the observation given in the console and assigns a label for the given observation.
  We assume that the number of features is the same as in the training data, there is no need to provide the correct label
c) exiting the program
The program should work for any input data provided in the form of a text file where:
- each line is a single observation
- each row contains N attributes separated by ","
- the first N-1 attributes are features of the observation and the last attribute is the decision attribute (correct label)
The program does not know the number of attributes N in advance, it determines it based on the loaded file.
Optionally, you can make a plot of accuracy against the number K - as a program option or separately, e.g. in Excel.
The program should be written independently. It is not possible to use ready-made libraries implementing machine learning algorithms.
The code (only the file with code not the whole project) should be placed in the appropriate task on the teams platform before classes and presented during classes.
Only programs that meet the described requirements will be checked!"""
import math
import sys

"""
We need to check if the given file is having right format of content.
"""

"""def is_file_ok(test_file_path, train_file_path):
    with open(test_file_path, 'r') as test_file, open(train_file_path, 'r') as train_file:
        for line_test, line_train in zip(test_file, train_file):
            content_test = line_test.split(",")
            content_train = line_train.split(",")
            if len(content_train) != 5:
                raise ValueError(f"The file '{train_file_path}' doesn't contain the valid attributes.")
"""            """if len(content_test) != 5 or not (
                    content_test[0].isdigit() and content_test[1].isdigit() and content_test[2].isdigit() and
                    content_train[3].isdigit() and content_train[4].isalpha()):
                raise ValueError(f"The file '{test_file_path}' doesn't contain the valid attributes.")
"""

"""
We will open both of the files and do the calculations with given number of K.
We will make calculations and put them into list
Depending on the given value of K we will check the main class is matching with the test class.
If so we will determine if it is true or not then return it.
"""

def find_majority_class(distance_list,given_k):
    distances = []
    class_names = []
    for i in range(0,len(distance_list)):
        distance_class = distance_list[i].split(":")
        distance = distance_class[0]
        class_name = distance_class[1]
        distances.append(distance)
        class_names.append(class_name)

    smallest_k_class_names = []
    for i in range(0,given_k):
        smallest_distance_index = distances.index(min(distances))
        smallest_class_name = class_names[smallest_distance_index]
        smallest_k_class_names.append(smallest_class_name)
        del distances[smallest_distance_index]
        del class_names[smallest_distance_index]

    name_dictionary = {}
    for name in smallest_k_class_names:
        if name in name_dictionary:
            name_dictionary[name] += 1
        else:
            name_dictionary[name] = 1
    most_repeated_name = max(name_dictionary, key=name_dictionary.get)
    return most_repeated_name



def find_distances(train_file_path, test_file_path, given_k):
    final_name_of_classes = []

    try:
        with open(test_file_path, 'r') as file_test:
            test_file_content = file_test.readlines()
        with open(train_file_path, 'r') as file_train:
            for i in range(0, len(test_file_content)):
                distances_classes = []
                test_content = []
                test_raw = test_file_content[i].strip().split(",")
                for k in range(0, len(test_raw)):
                    if k == len(test_raw) - 1:
                        test_content.append(str(test_raw[k]))
                    else:
                        test_content.append(float(test_raw[k]))
                for line in file_train:
                    train_content = []
                    train_raw = line.split(",")
                    for j in range(0, len(train_raw)):
                        if j == len(train_raw) - 1:
                            train_content.append(str(train_raw[j]))
                        else:
                            train_content.append(float(train_raw[j]))
                    first_value = (train_content[0] - test_content[0]) ** 2
                    second_value = (train_content[1] - test_content[1]) ** 2
                    third_value = (train_content[2] - test_content[2]) ** 2
                    forth_value = (train_content[3] - test_content[3]) ** 2
                    distance = math.sqrt(first_value + second_value + third_value + forth_value)
                    distances_classes.append(str(distance) + ":" + str(train_content[4]))
                majority_class = find_majority_class(distances_classes,given_k)
                final_name_of_classes.append(majority_class)

        answers = check_correctness_of_classes(final_name_of_classes)
        return answers

    except Exception as e:
        print(e)

def check_correctness_of_classes(final_name_of_classes,test_file_path):
    class_names_test = []
    with open(test_file_path) as file:
        for line in file:
            line_list = line.split(",")
            class_names_test.append(line_list[len(class_names_test) - 1])

    answers = []
    for i in range(0,len(final_name_of_classes)):
        if final_name_of_classes[i] == class_names_test[i]:
            answers.append(True)

    return answers


training_file = "/Users/demjrhan/Documents/nai-projects/project1/train.txt"
while True:
    print("A) use the test file \n"
          "B) provide your own test file \n"
          "C) exit the program. \n")
    user_input = str(input("enter a,b or c."))
    match user_input:
        case "a":
            test_file = str(input("enter test file path"))
            k_number = int(input("enter k"))
            answers = find_distances(training_file, test_file, k_number)
            print(answers)

            break
        case "b":
            training_file_path_b = str(input("enter test file path"))
            number_k_b = int(input("enter the K number"))
            break
        case "c":
            sys.exit()
