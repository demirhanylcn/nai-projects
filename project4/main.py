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
        label = stripped_line[-1]
        if label not in labels:
            labels.append(label)
    return labels


def find_centroids(labeled_lines):
    centroids = []
    length = len(labeled_lines[0].strip('\n').split(",")) - 2
    labels = find_labels(labeled_lines)
    find_label_percentage_in_each_centroid(labeled_lines, labels)
    for k_centroid in labels:
        centroid_k = []
        for i in range(length):
            total_sum = 0
            for j in range(len(labeled_lines)):
                stripped_line = labeled_lines[j].strip('\n').split(",")
                centroid = int(stripped_line[-1])
                if centroid == int(k_centroid):
                    total_sum += float(stripped_line[i])
            percentage = (total_sum / find_how_many_label(labeled_lines, int(k_centroid)))
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
                smallest_distance_index = j + 1
            elif distances[j][i] < smallest_distance_value:
                smallest_distance_value = distances[j][i]
                smallest_distance_index = j + 1
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

    print_purity(total_counts)


def print_purity(total_counts):
    count = 1
    for label in total_counts:
        cluster_string = str(count) + ".cluster"
        print(cluster_string , label)
        count += 1
def find_how_many_label(text, label):
    how_many_label = {}
    label = str(label)
    for line in text:
        stripped_line = line.strip('\n').split(",")
        if stripped_line[-1] not in how_many_label:
            how_many_label[stripped_line[-1]] = 0
        how_many_label[stripped_line[-1]] += 1

    return how_many_label[label]


def check_label_change(labeled_lines_before, labeled_lines_after):
    for line_before, line_after in zip(labeled_lines_before, labeled_lines_after):
        before_index = line_before.strip('\n').split(",")[-1]
        after_index = line_after.strip('\n').split(",")[-1]
        if before_index != after_index:
            return True
    return False


def sum_distances(labeled_lines_after, distances):
    labels = []
    distance_sum = 0
    for line in labeled_lines_after:
        stripped_line = line.strip('\n').split(",")
        labels.append(int(stripped_line[-1]))
    for each_distance in range(len(distances[0])):
        label = labels[each_distance]-1
        distance = distances[label][each_distance]
        distance_sum += distance
    return distance_sum



mac = "/Users/demjrhan/Documents/nai-projects/project4/iris_kmeans.txt"
windows = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project4\\iris_kmeans.txt"
if __name__ == "__main__":
    k_number = int(input("Enter the k: "))
    labeled_lines = initalize_labels(windows, k_number)
    iteration = 0
    while True:
        iteration += 1
        print(str(iteration) + ". iteration.")
        centroids, labeled_lines = find_centroids(labeled_lines)
        distances, labeled_lines = find_distances(centroids, labeled_lines)
        labeled_lines_after = change_labels(labeled_lines, distances)
        distances_sum = sum_distances(labeled_lines_after, distances)
        print("distance = ", distances_sum, "\n")
        is_Changed = check_label_change(labeled_lines, labeled_lines_after)
        if not is_Changed:
            break
        labeled_lines = labeled_lines_after
