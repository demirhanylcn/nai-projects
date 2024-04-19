import random


def initalize_labels(file_path,k_number):
    lines = read_file(file_path)
    labeled_lines = []
    for line in lines:
        labeled_lines.append(line.strip('\n') + "," + str(random.randint(1, k_number)))
    return labeled_lines


def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines

def find_centroids(labeled_lines,k_number):
    centroids = []
    # we are getting rid of last 2 column which represents label and centroid group
    length = len(labeled_lines[0].strip('\n').split(","))-2
    # count variable to make sure we go step by step each label then move on to next.


    percentage_of_iris = []
    each_centroid_iris = {}
    #reason of 1,k_number+1 because we wont have centroid with number 0, it is starting from 1.
    for k_centroid in range(1,k_number+1):
        # sum of values for dividing operation in the future
        sum = 0
        for i in range(length):
            for j in range(len(labeled_lines)):
                # we strip and split the line to have data like a,b,c,iris--,label
                stripped_line = labeled_lines[j].strip('\n').split(",")
                centroid = int(stripped_line[-1])
                if centroid == k_centroid:
                    sum += float(stripped_line[i])
                    group = stripped_line[-2]
                    if i == length - 1:
                        if group not in each_centroid_iris:
                            each_centroid_iris[group] = 0
                        each_centroid_iris[group] += 1
        percentage_of_iris.append(each_centroid_iris)
        each_centroid_iris = {}
        percentage = (sum / find_how_many_label(labeled_lines,k_centroid)) * 100
        print(percentage)
    print(percentage_of_iris)


def find_how_many_label(text,label):
    how_many_label = {}
    label = str(label)
    for lines in text:
        stripped_line = lines.strip('\n').split(",")
        if stripped_line[-1] not in how_many_label:
            how_many_label[stripped_line[-1]] = 0
        how_many_label[stripped_line[-1]] += 1

    if label not in how_many_label:
        raise ValueError("Label not found")
    return how_many_label[label]




if __name__ == "__main__":
    k_number = random.randint(2, 3)
    result = initalize_labels("C:\\Users\\demir\\Documents\\git\\nai-projects\\project4\\iris_kmeans.txt",k_number);
    find_centroids(result,k_number)
