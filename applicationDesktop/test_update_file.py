from tempfile import NamedTemporaryFile
import shutil
import csv

filename = 'Object.csv'
tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

with open(filename, 'r', newline='') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')

    for row in reader:
        row[1] = row[1].title()
        writer.writerow(row)
shutil.move(tempfile.name, filename)