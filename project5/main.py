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
        capacity = file.readline().strip("\n")

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


def get_optimal_vector(number,content,capacity):
    asd = get_characteristic_count(content)
if __name__ == '__main__':
    path = "C:\\Users\\demir\\Documents\\git\\nai-projects\\project5\\12"
    content = get_content(path)
    capacity = get_capacity(path)
    characteristic_count = get_characteristic_count(content)
    print(get_characteristic_vector(characteristic_count))


