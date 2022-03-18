from datetime import datetime as dt
import json as j

def period_aver(d1, d2):
    summ, count = 0, 0
    for i in marks:
        if int(d1.timestamp()) <= i["d"] <= int(d2.timestamp()):
            if i["m"].isnumeric():
                summ += int(i["m"])
                count += 1
    return round(summ / count, 3)


with open("output/data.json", "r", encoding="Windows-1251") as f:
    data = j.loads(f.read())

marks = []
for period in data:
    for lesson in period["lessons"]:
        marks += lesson["marks"]

marks = [{
    "m": m["mark"],
    "d": m["time"]
} for m in sorted(
    marks, key=lambda mark: int(mark["time"])
)]

print(period_aver(dt(2017, 9, 1), dt(2018, 6, 1)))
print(period_aver(dt(2018, 9, 1), dt(2019, 6, 1)))
print(period_aver(dt(2019, 9, 1), dt(2020, 6, 1)))
print(period_aver(dt(2020, 9, 1), dt(2021, 6, 1)))