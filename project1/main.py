
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
"""
We need to check if the given file is having right format of content.
"""

def is_file_ok(test_file_path, train_file_path):
    with open(test_file_path, 'r') as test_file, open(train_file_path, 'r') as train_file:
        for line_test, line_train in zip(test_file, train_file):
            content_test = line_test.strip().split(",")
            content_train = line_train.strip().split(",")
            if len(content_train) != 4 or not \
                    (content_train[0].isdigit() and content_train[1].isdigit() and content_train[2].isdigit() and
                    content_train[3].isalpha()):
                raise ValueError(f"The file '{train_file_path}' doesn't contain the valid attributes.")
            if len(content_test) != 4 or not (
                    content_test[0].isdigit() and content_test[1].isdigit() and content_test[2].isdigit() and
                    content_test[3].isalpha()):
                raise ValueError(f"The file '{test_file_path}' doesn't contain the valid attributes.")


"""
We will open both of the files and do the calculations with given number of K.
We will make calculations and put them into list
Depending on the given value of K we will check the main class is matching with the test class.
If so we will determine if it is true or not then return it.
"""


def calculations(train_file_path, test_file_path, given_k):
    distances = []
    final_name_of_classes = []
    classes = {}
    try:
        is_file_ok(test_file_path, train_file_path)
        with open(test_file_path, 'r') as file_test:
            test_file_content = file_test.readlines()
        with open(train_file_path, 'r') as file_train:
            for i in range(0, len(test_file_content)):
                for line in file_train:
                    content = line.split(",")
                    first_value = (float(content[0]) - float(test_file_content[i][0])) ** 2
                    second_value = (float(content[1]) - float(test_file_content[i][1])) ** 2
                    third_value = (float(content[2]) - float(test_file_content[i][2])) ** 2
                    distance = math.sqrt(first_value + second_value + third_value)
                    distances.append(str(distance) + ":" + str(content[3]))
                distances.sort()
                for each in range(0, len(given_k)):
                    _, name_of_class = str(each.split(":"))
                    if name_of_class in classes:
                        classes[name_of_class] += 1
                    else:
                        classes[name_of_class] = 1
                majority_class = max(classes, key=classes.get)
                final_name_of_classes.append(majority_class)
                classes.clear()
                distances.clear()
        return final_name_of_classes

    except Exception as e:
        print(e)


while True:
    print("A) use the test file \n"
          "B) provide your own test file \n"
          "C) exit the program. \n")
    user_input = input(str(input("enter a,b or c.")))
    match user_input:
        case "a":
            training_file_path_a = str(input("enter training file path"))
            number_k_a = int(input("enter the K number"))
        case "b":
            training_file_path_b = str(input("enter training file path"))
            number_k_b = int(input("enter the K number"))
        case "c":
            SystemExit
