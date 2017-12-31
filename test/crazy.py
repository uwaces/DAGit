import csv
p = dict()
with open('crazy.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    c = ord('A')
    for row in spamreader:
        p[c] = float(row[0]), float(row[1])
        c += 1

polygons = []
with open('crazy_p.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        polygons.append([p[ord(x)] for x in row])

print(polygons)
i = 0
for p in polygons:
        i += 1
        with open('crazy_poly'+str(i)+'.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for x in p:
                        spamwriter.writerow([x[0], x[1]])