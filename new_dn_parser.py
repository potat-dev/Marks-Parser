from bs4 import BeautifulSoup as soup
import dateparser as dp
import json as j

files = ["8-1", "8-2", "8-3", "8-4",
         "9-1", "9-2", "9-3", "9-4",
         "10-1", "10-2", "11-1", "11-2"]

def parse_file(file):
    lessons_data = []

    with open(file, "r", encoding="utf-8") as f:
        page = soup(f.read(), features="html.parser")
        table = page.find("table").find_all("tr")[2:]

    for row in table:
        data = row.find_all("td")
        name = data[1].find("strong").text
        prop, ills = (d.text for d in data[4:6])
        aver = data[6].find("span").text
        if aver == "": aver = "0"
        mark = aver if aver == "0" else data[7].find("span").text

        marks = sorted([
            {"mark"  : s.text,
             "work"  : s["title"].split(", ")[0],
             "date"  : s["title"].split(", ")[1],
             "time"  : int(dp.parse(s["title"].split(", ")[1]).timestamp()),
             "lesson": s["title"].split(", ")[2][0]
            } for s in data[2].find_all("span") +
                       data[2].find_all("a", {"class": "mark lsB"}) +
                       data[2].find_all("a", {"class": "mark lsR"})],
            key=lambda data: int(data["time"]))

        lessons_data.append({
            "name":  name,
            "aver":  aver,
            "mark":  mark,
            "prop":  prop,
            "ills":  ills,
            "marks": marks
        })

    return lessons_data

marks_data = []
for f in files:
    marks_data.append({
        "name": f,
        "form": f.split("-")[0],
        "period": f.split("-")[1],
        "lessons": parse_file("marks_data/" + f + ".html")
    })

with open("parsed_marks_data.json", "w") as out_file:
    out_file.write(j.dumps(marks_data, indent=2, ensure_ascii=False))

with open("data.json", "w") as out_file:
    out_file.write(j.dumps(marks_data, ensure_ascii=False))