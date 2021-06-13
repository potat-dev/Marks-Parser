from bs4 import BeautifulSoup as soup
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
        late, prop, ills = (d.text for d in data[3:6])
        aver = data[6].find("span").text
        if aver == "": aver = "0"
        mark = aver if aver == "0" else data[7].find("span").text

        marks = [[s.text] + s["title"].split(", ") for s in data[2].find_all("span")]
        props = [[s.text] + s["title"].split(", ") for s in data[2].find_all("a", {"class": "mark lsB"})]

        lesson = {
            "name":  name,
            "aver":  aver,
            "mark":  mark,
            "late":  late,
            "prop":  prop,
            "ills":  ills,
            "marks": marks,
            "prips": props
        }
        lessons_data.append(lesson)

    return lessons_data


out = parse_file("marks_data/" + files[-1] + ".html")
print(j.dumps(out, indent=2, ensure_ascii=False))