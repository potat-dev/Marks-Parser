from bs4 import BeautifulSoup as soup
import rutimeparser as rutime
import dateparser as dp
import json as j

def parse_file(file):
    lessons_data = []

    with open(file, "r", encoding="utf-8") as f:
        page = soup(f.read(), features="html.parser")
        table = page.find("table").find_all("tr")[2:]

    for row in table[:1]:
        data = row.find_all("td")
        name = data[1].find("strong").text
        late, prop, ills = (d.text for d in data[3:6])
        aver = data[6].find("span").text
        if aver == "": aver = "0"
        mark = aver if aver == "0" else data[7].find("span").text

      #  marks = [[s.text] + s["title"].split(", ") for s in data[2].find_all("span")]
      #  props = [[s.text] + s["title"].split(", ") for s in data[2].find_all("a", {"class": "mark lsB"})]

        marks = sorted(
            [{"mark": s.text,
              "work": s["title"].split(", ")[0],
              "date": s["title"].split(", ")[1],
              "time": int(dp.parse(s["title"].split(", ")[1]).timestamp()),
              "lesson": s["title"].split(", ")[2][0]
             } for s in data[2].find_all("span") +
                        data[2].find_all("a", {"class": "mark lsB"})],
            key=lambda data: int(data["time"]))

       # sorted(student_tuples, key=lambda student: student[2])
       # props = [[s.text] + s["title"].split(", ") for s in data[2].find_all("a", {"class": "mark lsB"})]

        lesson = {
            "name" : name,
           # "aver" : aver,
           # "mark" : mark,
            "late" : late,
            "prop" : prop,
            "ills" : ills,
            "marks": marks,
          #  "props": props
        }
        lessons_data.append(lesson)

    return lessons_data


out = parse_file("marks_data/11-2.html")
print(j.dumps(out, indent=2, ensure_ascii=False))



'''
# print(int(dp.parse('10 июля 2021 г. в 7:45').timestamp()))
from datetime import datetime
import locale

date_string = "Добавлено: суббота, 26 декабря 2015 г. в 11:01:59"
locale.setlocale(locale.LC_TIME, "rus")
d = {'января': 'январь', 'декабря': 'декабрь'}
for k, v in d.items():
    date_string = date_string.replace(k, v)
ru_date_object = datetime.strptime(date_string , 'Добавлено: %A, %d %B %Y г. в %H:%M:%S')
print(ru_date_object)

  <td class="tac" style="text-align:left;">
  	<span title="Ответ на уроке, 8 сентября 2020, 2 урок ">4</span> 
  	<span title="Ответ на уроке, 10 сентября 2020, 3 урок ">5</span> 
  	<span data-id="1721324053045889853" data-num="0" data-work_id="1719483633789762077" title="Самостоятельная работа, 10 сентября 2020, 4 урок ">5-</span>
  	<span class="mark mY analytics-app-popup-mark" data-id="1759957790679554399" title="Самостоятельная работа, 24 декабря 2020, 3 урок ">3</span>
  </td>
'''