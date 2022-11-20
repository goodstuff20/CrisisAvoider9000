import csv
import random


def prices():
    base = random.randrange(100000, 1000000)
    prev2 = base * (1 + random.randrange(-2, 8) / 100)
    prev3 = prev2 * (1 + random.randrange(-2, 8) / 100)
    return [base, int(prev2), int(prev3)]


def risks(bundesland):
    if bundesland == "Freistaat Bayern" or bundesland == "Niedersachsen":
        base = random.randrange(1, 6)
        prev = base + random.randrange(1, 4)
        prev2 = prev + random.randrange(1, 3)
    else:
        base = random.randrange(1, 4)
        prev = base + random.randrange(0, 4)
        prev2 = prev + random.randrange(0, 3)
    return [base / 100, min(max(prev, 0), 100) / 100, min(max(prev2, 0), 100) / 100]


if __name__ == '__main__':
    with open("Liste-Staedte-in-Deutschland.csv", newline="") as file, open("CityData.csv", "w", newline="") as output:
        reader = csv.reader(file, delimiter=';')
        writer = csv.writer(output, delimiter=';')
        writer.writerow(["Stadt","Bundesland","prev_price1","prev_price2","prev_price3","prev_risk1","prev_risk2","prev_risk3","Houselive","Buyout"])
        next(reader)
        for row in reader:
            writerow = [row[1]]
            writerow += [row[3].lstrip(' ')]
            writerow += prices()
            writerow += risks(row[3].lstrip(' '))
            writerow += [random.randrange(5, 23)]
            writerow += [random.randrange(9, 70)]
            writer.writerow(writerow)