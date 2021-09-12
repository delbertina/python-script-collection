from tkinter.filedialog import askopenfilename
from shapely import geometry
import re


# Regex string for the header of each section
search_regex_header = r'.+:$'
# Regex string for a data line under a header
search_regex_data = r'- {x: (-?[0-9]{1,4}), z: (-?[0-9]{1,4})'
# Input file
file_in = askopenfilename()
# Output file for blocks
file_out_block = open("out-block.txt", "wt")
# Output file for containers
file_out_container = open("out-container.txt", "wt")
# Array of polygons with array of points
polygons = []
# Array of polygon bounds; Update later to gather this data dynamically
quadrants = [[-6000, 200, -6000, 0], [0, 6000, -6000, 0], [-6000, 200, 0, 6000], [0, 6000, 0, 6000]]
# Start point of query line
z1 = None
# End point of query line
z2 = None
# If the current line has been submitted
isSubmitted = True

# for each line in the file
with open(file_in, 'r') as foundFile:
    for line in foundFile:
        isHeader = re.search(search_regex_header, line)
        isData = re.search(search_regex_data, line)
        # if line is a header
        if isHeader:
            # then add an empty container to the array
            polygons.append([])
        # else if line is a data
        elif isData:
            # then parse and add coord to last array
            polygons[-1].append(geometry.Point(int(isData.group(1)), int(isData.group(2))))
print('File parse done!')

# For each of the 4 polygons; Update later to do dynamically
for a in range(0, 4):
    poly = geometry.Polygon([[p.x, p.y] for p in polygons[a]])
    # Check only the specific bounds of the polygon
    for x in range(quadrants[a][0], quadrants[a][1]):
        # Log every 100
        if x % 100 == 0:
            print('Quadrant ' + str(a+1) + ' progress: ' + str(x)
                  + ' in range ' + str(quadrants[a][0]) + ' -> ' + str(quadrants[a][1]))
        for z in range(quadrants[a][2], quadrants[a][3]):
            # If the point is contained in the polygon
            if poly.contains(geometry.Point(x, z)):
                # If should start new entry
                if isSubmitted:
                    z1 = z
                    z2 = z
                    isSubmitted = False
                # Else just update
                else:
                    z2 = z
            # Else the point is not within the polygon
            else:
                # If the current line has not been submitted yet
                if not isSubmitted:
                    # Close out and write to file
                    isSubmitted = True
                    file_out_block.write(
                        "DELETE FROM co_block WHERE x=" + str(x)
                        + " AND z>=" + str(z1) + ' AND z<=' + str(z2) + ';\n')
                    file_out_container.write(
                        "DELETE FROM co_container WHERE x=" + str(x)
                        + " AND z>=" + str(z1) + ' AND z<=' + str(z2) + ';\n')
        # If z for loop finished without submitting line
        if not isSubmitted:
            # Close out and write to file
            isSubmitted = True
            file_out_block.write(
                "DELETE FROM co_block WHERE x=" + str(x)
                + " AND z>=" + str(z1) + ' AND z<=' + str(z2) + ';\n')
            file_out_container.write(
                "DELETE FROM co_container WHERE x=" + str(x)
                + " AND z>=" + str(z1) + ' AND z<=' + str(z2) + ';\n')
    print('Quadrant ' + str(a+1) + ' has been completed')
print('Complete!')
file_out_block.close()
file_out_container.close()
