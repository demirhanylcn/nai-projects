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


def is_file_ok(test_file_path, train_file_path):
    with open(test_file_path, 'r') as test_file, open(train_file_path, 'r') as train_file:
        for line_test, line_train in zip(test_file, train_file):
            content_test_raw = line_test.strip().split(",")
            content_train_raw = line_train.strip().split(",")

            content_test_calculated = []
            for i in range(len(content_test_raw)):
                if i == len(content_test_raw) - 1:
                    content_test_calculated.append(str(content_test_raw[i]))
                else:
                    content_test_calculated.append(float(content_test_raw[i]))

            content_train_calculated = []
            for j in range(len(content_train_raw)):
                if j == len(content_train_raw) - 1:
                    content_train_calculated.append(str(content_train_raw[j]))
                else:
                    content_train_calculated.append(float(content_train_raw[j]))



            if len(content_train_calculated) != len(content_test_calculated):
                raise ValueError(
                    f"The files '{test_file_path}' and '{train_file_path}' don't contain the same number of attributes.")

            for test_value in content_test_calculated[:-1]:
                if not isinstance(test_value, float):
                    raise ValueError(f"The file '{test_file_path}' doesn't contain valid numerical attributes.")

            for train_value in content_train_calculated[:-1]:
                if not isinstance(train_value, float):
                    raise ValueError(f"The file '{train_file_path}' doesn't contain valid numerical attributes.")

            if not isinstance(content_test_calculated[-1], str):
                raise ValueError(f"The file '{test_file_path}' doesn't contain a valid attribute as the last element.")

            if not isinstance(content_train_calculated[-1], str):
                raise ValueError(f"The file '{train_file_path}' doesn't contain a valid attribute as the last element.")


def main_file(train_file_path, test_file_path, given_k):


    try:

        is_file_ok(test_file_path, train_file_path)
        with open(test_file_path, 'r') as file_test:
            test_file_content = file_test.readlines()
        with open(train_file_path, 'r') as file_train:
            train_file_content = file_train.readlines()

        final_answers = []

        for test_file_count in range(0, len(test_file_content)):
            distances_names = find_distances_classes(test_file_content, train_file_content, test_file_count)
            print(sorted(distances_names.copy()))
            final_class = find_final_class(distances_names, given_k)
            answer = check_correctness_of_classes(final_class, test_file_count, test_file_content)
            final_answers.append(answer)

        return final_answers
    except ValueError as e:
        print(e)




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

        calculations = []
        total_sum = 0
        for k in range(len(test_file_content_calculated)-1):
            value = (train_file_content_calculated[k] - test_file_content_calculated[k]) ** 2
            calculations.append(value)
        for value in calculations:
            total_sum += value
        distance = math.sqrt(total_sum)
        distances_classes.append(str(distance) + ":" + str(train_file_content_calculated[len(train_file_content_calculated) - 1]))

    return distances_classes


def find_minimum_index(distance_list, given_k):
    min_index_list = []
    distance_list_copy = distance_list.copy()

    for i in range(given_k):
        min_number = min(distance_list_copy)
        min_index = distance_list_copy.index(min_number)

        min_index_list.append(min_index)
        distance_list_copy[min_index] = float('inf')

    return min_index_list


def find_final_class(distances_classes, given_k):
    distances = []
    class_names = []
    for i in range(len(distances_classes)):
        distance_class = distances_classes[i].split(":")
        distance = float(distance_class[0])
        class_name = str(distance_class[1])
        distances.append(distance)
        class_names.append(class_name)

    minimum_indexes = find_minimum_index(distances, given_k)
    final_class_names = []

    for j in range(len(minimum_indexes)):
        final_class = class_names[minimum_indexes[j]]
        final_class_names.append(final_class)

    final_class_dictionary = {}
    for name in final_class_names:
        if name in final_class_dictionary:
            final_class_dictionary[name] += 1
        else:
            final_class_dictionary[name] = 1

    most_repeated_names = []
    max_count = 0
    for name, count in final_class_dictionary.items():
        if count > max_count:
            most_repeated_names = [name]
            max_count = count
        elif count == max_count:
            most_repeated_names.append(name)

    if len(most_repeated_names) > 1:
        most_repeated_name = "X"
    else:
        most_repeated_name = most_repeated_names[0]

    return most_repeated_name


def check_correctness_of_classes(final_class, test_file_count, test_file_content):
    test_file_line_list = test_file_content[test_file_count].strip().split(",")
    test_file_class_name = test_file_line_list[len(test_file_line_list) - 1]
    print("test_file_class_name = ", test_file_class_name)
    print("final_class = ", final_class)
    if test_file_class_name == final_class:
        return True
    else:
        return False


training_file = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project1\\train.txt"
test_file = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project1\\test.txt"
given_test_file = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project1\\givenTest.txt"

def write_into_file(file_content):

    with open("givenTest.txt", "w") as file:
        for line in file_content:
            file.write(line + "\n")
while True:
    print("\nA) use the test file \n"
          "B) provide your own test file \n"
          "C) exit the program. \n")
    user_input = str(input("enter a,b or c. \nyour input = "))
    match user_input.lower().strip()[0]:
        case "a":
            test_file_path = str(input("enter test file path = "))
            k_number = int(input("enter the K number = "))
            answers = main_file(training_file, test_file, k_number)
            print(answers)

        case "b":
            count = 0
            data = []
            while True:
                print("to stop write stop.")
                line = str(input("enter line" + str(count) + " = "))
                if line.lower() == "stop":
                    break
                else:
                    data.append(line)
                    count+=1
            k_number = int(input("enter the K number = "))
            write_into_file(data)
            answers = main_file(training_file, given_test_file, k_number)
            print(answers)

        case "c":
            sys.exit()
