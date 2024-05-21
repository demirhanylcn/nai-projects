def get_content(path):
    content = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            if line.strip():
                line = line.strip("\n").split(" ")
                content.append(line)
    return content



def get_capacity(path):
    with open(path, 'r') as file:
        capacity = int(file.readline().strip("\n"))

    return capacity

def get_characteristic_count(content):
    count = pow(2, len(content))
    return count-1

def get_characteristic_vector(number):
    if number == 0:
        return [0]

    binary_representation = []
    while number > 0:
        remainder = number % 2
        binary_representation.insert(0, remainder)
        number = number // 2

    while len(binary_representation) < 30:
        binary_representation.insert(0, 0)

    return binary_representation


def check_fitting_knapsack(characteristic_vector, content, capacity):
    total_weight = 0

    for index in range(0,len(characteristic_vector)):
        if characteristic_vector[index] == 1:
            total_weight += int(content[index][0])
    if total_weight <= capacity:
        return True

    return False


def get_total_value(characteristic_vector, content):
    total_value = 0
    for index in range(0, len(characteristic_vector)):
        if characteristic_vector[index] == 1:
            total_value += int(content[index][1])
    return total_value
def get_optimal_vector(max_number, content, capacity):
    number = 0

    old_value = -999999
    optimal_vector = []
    while number in range(0, max_number+1):
        characteristic_vector = get_characteristic_vector(number)
        if check_fitting_knapsack(characteristic_vector, content, capacity):
            total_value = get_total_value(characteristic_vector, content)
            if total_value > old_value:
                optimal_vector = characteristic_vector
        number += 1
    return optimal_vector







if __name__ == '__main__':
    path = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project5\\12.txt"
    content = get_content(path)
    capacity = get_capacity(path)
    characteristic_count = get_characteristic_count(content)
    print(get_optimal_vector(characteristic_count, content, capacity))
