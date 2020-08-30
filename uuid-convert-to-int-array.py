from tkinter.filedialog import askopenfilename
import re


def twos_complement(hex_string, bits):
    value = int(hex_string, 16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value


def hex_to_int_array(hex_input):
    array_index_0 = twos_complement(hex_input.group(1), 32)
    array_index_1 = twos_complement(hex_input.group(2) + hex_input.group(3), 32)
    array_index_2 = twos_complement(hex_input.group(4) + hex_input.group(5), 32)
    array_index_3 = twos_complement(hex_input.group(6), 32)
    # Compile return array
    return_string = \
        "[I;" + str(array_index_0) \
        + ',' + str(array_index_1) \
        + ',' + str(array_index_2) \
        + ',' + str(array_index_3) + ']'
    return return_string


# Regex string
search_regex = r'"([a-f0-9]{8})-([a-f0-9]{4})-([a-f0-9]{4})-([a-f0-9]{4})-([a-f0-9]{4})([a-f0-9]{8})"'
# Input file
file_in = askopenfilename()
# Output file to write the result to
file_out = open("out.txt", "wt")
# for each line in the input file
with open(file_in, 'r') as foundFile:
    for line in foundFile:
        # read replace the string and write to output file
        file_out.write(re.sub(search_regex, hex_to_int_array, line))
# Close input and output files
file_out.close()
