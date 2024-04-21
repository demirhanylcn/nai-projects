import math
import random


def initalize_labels(file_path, k_number):
    lines = read_file(file_path)
    labeled_lines = []
    for line in lines:
        labeled_lines.append(line.strip('\n') + "," + str(random.randint(1, k_number)))
    return labeled_lines


def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines

def find_labels(labeled_lines):
    labels = []
    for line in labeled_lines:
        stripped_line = line.strip('\n').split(",")
        label = labels.append(stripped_line[-1])
        if label not in labels:
            labels.append(label)
    return labels;
def find_centroids(labeled_lines, k_number):
    centroids = []
    # we are getting rid of last 2 column which represents label and centroid group
    length = len(labeled_lines[0].strip('\n').split(",")) - 2
    # count variable to make sure we go step by step each label then move on to next.
    labels = find_labels(labeled_lines)
    find_label_percentage_in_each_centroid(labeled_lines, labels)

    #reason of 1,k_number+1 because we wont have centroid with number 0, it is starting from 1.
    for k_centroid in labels:
        # sum of values for dividing operation in the future
        centroid_k = []
        for i in range(length):
            sum = 0
            for j in range(len(labeled_lines)):
                # we strip and split the line to have data like a,b,c,iris--,label
                stripped_line = labeled_lines[j].strip('\n').split(",")
                centroid = int(stripped_line[-1])
                if centroid == k_centroid:
                    sum += float(stripped_line[i])
            percentage = (sum / find_how_many_label(labeled_lines, k_centroid))
            centroid_k.append(percentage)
        centroids.append(centroid_k)
    return centroids, labeled_lines


def find_distances(centroids, labeled_lines):
    distance_list = []
    centroid_distances = []

    for centroid in centroids:
        for line in labeled_lines:
            distance = 0
            stripped_line = line.strip('\n').split(",")
            for j in range(len(stripped_line) - 2):
                distance += (float(centroid[j]) - float(stripped_line[j])) ** 2
            centroid_distances.append(distance)
        distance_list.append(centroid_distances)
        centroid_distances = []
    return distance_list, labeled_lines


def change_labels(labeled_lines, distances):
    new_labeled_lines = []
    for i in range(len(labeled_lines)):
        stripped_line = labeled_lines[i].strip('\n').split(",")
        smallest_distance_index = 0
        smallest_distance_value = float("inf")
        for j in range(len(distances)):
            if j == 0:
                smallest_distance_value = distances[j][i]
                smallest_distance_index = j+1
            elif distances[j][i] < smallest_distance_value:
                    smallest_distance_value = distances[j][i]
                    smallest_distance_index = j+1
        new_line = ""
        for k in range(len(stripped_line)):
            if k == len(stripped_line) - 1:
                new_line += str(smallest_distance_index)
            else:
                new_line += stripped_line[k] + ","
        new_labeled_lines.append(new_line)
    return new_labeled_lines



def find_label_percentage_in_each_centroid(text, labels):
    total_counts = []
    for k in labels:
        label_count = {}
        count = 0
        for line in text:
            stripped_line = line.strip('\n').split(",")
            if stripped_line[-1] == str(k):
                label = stripped_line[-2]
                if label not in label_count:
                    label_count[label] = 0
                label_count[label] += 1
                count += 1
        total_counts.append(label_count)

    for centroid in total_counts:
        total_sum = sum(centroid.values())
        for label in centroid:
            centroid[label] = (float(centroid[label]) / total_sum) * 100

    print(total_counts)


def find_how_many_label(text, label):
    how_many_label = {}
    label = str(label)
    for line in text:
        stripped_line = line.strip('\n').split(",")
        if stripped_line[-1] not in how_many_label:
            how_many_label[stripped_line[-1]] = 0
        how_many_label[stripped_line[-1]] += 1

    print("Counts for each label:", how_many_label)

    if label not in how_many_label:
        raise ValueError(f"Label '{label}' not found in the data. Available labels: {list(how_many_label.keys())}")
    return how_many_label[label]


def check_label_change(labeled_lines_before, labeled_lines_after):
    for line_before, line_after in zip(labeled_lines_before, labeled_lines_after):
        before_index = line_before.strip('\n').split(",")[-1]
        after_index = line_after.strip('\n').split(",")[-1]
        if before_index != after_index:
            return True
    return False


mac = "/Users/demjrhan/Documents/nai-projects/project4/iris_kmeans.txt"
windows = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project4\\iris_kmeans.txt"
if __name__ == "__main__":
    k_number = random.randint(2, 10)
    labeled_lines = initalize_labels(mac, k_number)
    while True:
        centroids, labeled_lines = find_centroids(labeled_lines, k_number)
        distances, labeled_lines = find_distances(centroids, labeled_lines)
        print(distances)
        labeled_lines_after = change_labels(labeled_lines, distances)
        is_Changed = check_label_change(labeled_lines, labeled_lines_after)
        if is_Changed == False:
            break
        labeled_lines = labeled_lines_after
