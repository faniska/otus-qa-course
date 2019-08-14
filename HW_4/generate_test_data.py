from itertools import product


def get_file_lines(file_path):
    lines = []
    data = open(file_path)
    for file_line in data:
        lines.append(list(map(lambda s: s.strip(), file_line.split(','))))
    return lines


file_lines = get_file_lines('data.csv')

# Collect all person names
person_list = [l[0] for l in file_lines]

# Collect all city names
city_list = [l[1] for l in file_lines]

# Generate +/- variants for 3 columns
boolean_variants = list(product(['+', '-'], repeat=3))

with open('data_output.csv', 'w') as output_data:
    for person in person_list:
        for city in city_list:
            for variant in boolean_variants:
                line = [person, city] + list(variant)
                output_data.write(','.join(line) + "\n")
