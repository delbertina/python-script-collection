from tkinter.filedialog import askopenfilename
import re


def give_to_item_object(cmd_input):
    if cmd_input:
        return '  ' + 'Skull-' + str(line_index) + ':\n'\
               + '    ' + 'Amount: 1\n'\
               + '    ' + 'Name: "' + cmd_input.group(1) + '"\n'\
               + '    ' + 'Material: \'PLAYER_HEAD\'\n'\
               + '    ' + 'SkullTexture: ' + '\'' + cmd_input.group(2) + '\'\n'
    return ''


# Line Index
line_index = 0
# Regex string
search_regex = r'\\"text\\":\\"([a-zA-Z0-9:() ]{3,})\\"[\S\s]{3,}"([a-zA-Z0-9+\/=]{170,190})"'
# Input file
file_in = askopenfilename()
# Output file to write the result to
file_out = open("out.txt", "wt")
# for each line in the input file
with open(file_in, 'r') as foundFile:
    file_out.write('RandomItem:\n')
    for line in foundFile:
        # read replace the string and write to output file
        file_out.write(give_to_item_object(re.search(search_regex, line)))
        line_index += 1
# Close input and output files
file_out.close()
