import csv
# read csv file and return a list of lines
def readCSV(filepath):
    lines = []
    with open(filepath) as csvfile:
        # strip white spaces
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            # remove empty spaces
            row = [x.strip() for x in row]
            lines.append(row)
    return lines