#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <string>
#include <chrono>

std::vector<std::vector<int>> get_content(const std::string &path) {
    std::vector<std::vector<int>> content;
    std::ifstream file(path);
    std::string line;

    // first line is capacity so skipping it
    std::getline(file, line);

    while (std::getline(file, line)) {
        if (!line.empty()) {
            int weight = std::stoi(line.substr(0, line.find(' ')));
            int value = std::stoi(line.substr(line.find(' '), line.size()));
            std::vector<int> row = {weight, value};
            content.push_back(row);
        }
    }
    return content;
}

int get_capacity(const std::string &path) {
    std::ifstream file(path);
    std::string line;
    std::getline(file, line);
    return std::stoi(line);
}


int get_characteristic_count(const std::vector<std::vector<int>> &content) {
    return pow(2, content.size()) - 1;
}

std::vector<int> get_characteristic_vector(int number, int size) {
    std::vector<int> binary_representation(size, 0);
    for (int i = size - 1; i >= 0 && number > 0; --i) {
        binary_representation[i] = number % 2;
        number /= 2;

    }

    return binary_representation;
}


bool check_fitting_knapsack(const std::vector<int> &characteristic_vector, const std::vector<std::vector<int>> &content,
                            int capacity) {
    int total_weight = 0;
    for (int i = 0; i < characteristic_vector.size(); ++i) {
        if (characteristic_vector[i] == 1) {
            total_weight += content[i][0];
        }
    }
    return total_weight <= capacity;
}


int get_total_value(const std::vector<int> &characteristic_vector, const std::vector<std::vector<int>> &content) {
    int total_value = 0;
    for (int i = 0; i < characteristic_vector.size(); ++i) {
        if (characteristic_vector[i] == 1) {
            total_value += content[i][1];
        }
    }
    return total_value;
}


std::vector<int> get_optimal_vector(int max_number, const std::vector<std::vector<int>> &content, int capacity) {
    int old_value = -999999;
    std::vector<int> optimal_vector;
    int size = content.size();
    for (int number = 0; number <= max_number; ++number) {
        std::vector<int> characteristic_vector = get_characteristic_vector(number, size);
        if (check_fitting_knapsack(characteristic_vector, content, capacity)) {
            int total_value = get_total_value(characteristic_vector, content);
            if (total_value > old_value) {
                old_value = total_value;
                optimal_vector = characteristic_vector;
            }
        }
    }
    return optimal_vector;
}

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    std::string path = "C:\\Users\\demir\\CLionProjects\\untitled2\\12.txt";
    std::vector<std::vector<int>> content = get_content(path);

    int capacity = get_capacity(path);
    int characteristic_count = get_characteristic_count(content);
    std::vector<int> optimal_vector = get_optimal_vector(characteristic_count, content, capacity);

    for (int val: optimal_vector) {
        std::cout << val << " ";
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "execution time " << elapsed;

    return 0;
}
