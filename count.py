import csv

r = csv.reader(open('comments.csv'))
lines = [l for l in r]
print lines[len(lines)-1][0]