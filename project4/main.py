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
    find_label_percentage_in_each_centroid(labeled_lines,k_number)


    #reason of 1,k_number+1 because we wont have centroid with number 0, it is starting from 1.
    for k_centroid in range(1,k_number+1):
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
    print(centroids)


def find_label_percentage_in_each_centroid(text, k_number):
    total_counts = []
    for k in range(1, k_number+1):
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
