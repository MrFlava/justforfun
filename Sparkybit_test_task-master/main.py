
# reading data
source = open('source.txt', 'r')

# writing data
output = open('output.txt', 'w')


def fibonacci_sequence(source, output):
    # getting data from source
    source_data = source.read().splitlines()
    source.close()

    # getting line indexes from source
    line_indexes = [source_data.index(i) + 1 for i in source_data]
    first_element = second_element = line_indexes[0]
    counter_value = 2

    sequence_elements = [first_element]

    for i in range(line_indexes[0], line_indexes[6]):
        # code for fibonacci sequence
        while counter_value < line_indexes.index(i) + 1:

            elements_sum = first_element + second_element
            first_element = second_element
            second_element = elements_sum
            counter_value += 1
            # adding fibonacci sequence to list
            sequence_elements.append(elements_sum)

    # checking for right index between sequence_elements and source_data
    for i in source_data:

        for element in sequence_elements:

            if source_data.index(i) == element-1:
                # reverse and writing data in output.txt
                output.write(i[::-1] + '\n')

    output.close()

    return 'Data loaded successfully!'


print(fibonacci_sequence(source, output))
