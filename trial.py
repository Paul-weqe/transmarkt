import csv
import pprint

with open("/home/waswa/players.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    next(spamreader)
    info = next(spamreader)
    print(", ".join(info))