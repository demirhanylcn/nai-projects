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


def main_file(train_file_path, test_file_path, given_k):
    with open(test_file_path, 'r') as file_test:
        test_file_content = file_test.readlines()
    with open(train_file_path, 'r') as file_train:
        train_file_content = file_train.readlines()

    final_answers = []

    for test_file_count in range(len(test_file_content)):
        distances_names = find_distances_classes(test_file_content, train_file_content,test_file_count)
        final_class = find_final_class(distances_names, given_k)
        answer = check_correctness_of_classes(final_class, test_file_count,test_file_content)
        final_answers.append(answer)

    return final_answers


def find_distances_classes(test_file_content, train_file_content, test_file_count):
    distances_classes = []

    test_file_raw_content = test_file_content[test_file_count].strip().split(",")
    test_file_content_calculated = []

    for i in range(len(test_file_raw_content)):
        if i == len(test_file_raw_content) - 1:
            test_file_content_calculated.append(str(test_file_raw_content[i]))
        else:
            test_file_content_calculated.append(float(test_file_raw_content[i]))

    for i in range(len(train_file_content)):
        train_file_line_raw_content = train_file_content[i].strip().split(",")
        train_file_content_calculated = []
        for j in range(len(train_file_line_raw_content)):
            if j == len(train_file_line_raw_content) - 1:
                train_file_content_calculated.append(str(train_file_line_raw_content[j]))
            else:
                train_file_content_calculated.append(float(train_file_line_raw_content[j]))

        first_value = (train_file_content_calculated[0] - test_file_content_calculated[0]) ** 2
        second_value = (train_file_content_calculated[1] - test_file_content_calculated[1]) ** 2
        third_value = (train_file_content_calculated[2] - test_file_content_calculated[2]) ** 2
        forth_value = (train_file_content_calculated[3] - test_file_content_calculated[3]) ** 2
        distance = math.sqrt(first_value + second_value + third_value + forth_value)
        distances_classes.append(str(distance) + ":" + str(train_file_content_calculated[4]))

    return distances_classes

def find_minimum_index(distance_list, given_k):
    min_index_list = []

    for k in range(given_k):
        min_number = distance_list[0]
        min_index = 0

        for i in range(1, len(distance_list)):
            if distance_list[i] < min_number:
                min_number = distance_list[i]
                min_index = i

        min_index_list.append(min_index)

    return min_index_list
def find_final_class(distances_classes,given_k):
    distances = []
    class_names = []
    for i in range(len(distances_classes)):
        distance_class = distances_classes[i].split(":")
        distance = float(distance_class[0])
        class_name = str(distance_class[1])
        distances.append(distance)
        class_names.append(class_name)

    minimum_indexes = find_minimum_index(distances,given_k)
    final_class_names = []
    for i in range(len(class_names)):
        if i in minimum_indexes:
            final_class_names.append(class_names[i])

    final_class_dictionary = {}
    for name in final_class_names:
        if name in final_class_dictionary:
            final_class_dictionary[name] += 1
        else:
            final_class_dictionary[name] = 1
    most_repeated_name = max(final_class_dictionary, key=final_class_dictionary.get)
    return most_repeated_name

def check_correctness_of_classes(final_class,test_file_count,test_file_content):
    test_file_line_list = test_file_content[test_file_count].strip().split(",")
    test_file_class_name = test_file_line_list[len(test_file_line_list)-1]
    print(test_file_class_name,final_class)
    if test_file_class_name == final_class:
        return True
    else:
        return False

training_file = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project1\\train.txt"
test_file = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project1\\test.txt"

while True:
    print("A) use the test file \n"
          "B) provide your own test file \n"
          "C) exit the program. \n")
    user_input = str(input("enter a,b or c."))
    match user_input.lower().strip()[0]:
        case "a":
            test_file = test_file
            k_number = int(input("enter k"))
            answers = main_file(training_file, test_file, k_number)
            print(answers)

            break
        case "b":
            training_file_path_b = str(input("enter test file path"))
            number_k_b = int(input("enter the K number"))
            break
        case "c":
            sys.exit()
