import time
import datetime
import requests
import threading
import json

def load_pass(path):
    with open(path) as file:
        return json.load(file)


class Edu:
    def __init__(self, web_addr: str, acc_name: str, acc_pass: str, enable_threading=True):
        if enable_threading:
            self.thread = threading.Thread(target=self.run)
            self.thread.daemon = False
            self.thread.start()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
        self.account = {"username": acc_name, "password": acc_pass}
        self.edupage_address = web_addr
        self.name = acc_name
        self.password = acc_pass
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.session = requests.session()
        self.session.post(self.edupage_address + "login/edubarLogin.php", data=self.account, headers=self.headers)
        self.gsh = self.session.get("https://spspb.edupage.org/timeline/"
                                    , headers=self.headers).text.split("\n")[60].split('"')[1]

        self.substitutions = None

    def run(self):
        time.sleep(1)
        while True:
            self.substitutions = self.get_substitutions()
            time.sleep(5)

    def get_substitutions(self):
        substitutions = self.session.post(self.edupage_address + "substitution/server/viewer.js?__func"
                                                                 "=getSubstViewerDayDataHtml",
                                          data='{"__args":[null,{"date":"2021-06-22","mode":"classes"}],"__gsh": "' + self.gsh + '"}')
        list_parsed = substitutions.json()["r"].split("""<span class=\"print-font-resizable\">""")
        del list_parsed[0]
        for position, line in enumerate(list_parsed):
            list_parsed[position] = line.split("</span>")[0]
        chybajuci_uc = list_parsed[0]
        del list_parsed[0]
        if list_parsed[1] == "Na tento deň nie sú zadané žiadne suplovania.":
            return {"chybajuci": "Nikto", "info": list_parsed[1]}
        else:
            list_triedy = {}
            trieda = "info"
            for position, line in enumerate(list_parsed):
                if len(line) < 7:
                    try:
                        int(line)
                    except:
                        if "(" and ")" not in line:
                            trieda = line
                            list_triedy[line] = {}
                if trieda == None:
                    raise LookupError("Invalid substitution data")
                if len(line) > 7 and line != "celý deň":
                    if line == '<img src="/global/pics/ui/absent_32.svg" style="height:16px;display:inline-block;vertical-align:text-bottom;margin-right:5px"/>Chýba':
                        list_triedy[trieda][list_parsed[position - 1]] = "Chýba"
                    else:
                        list_triedy[trieda][list_parsed[position - 1]] = line
            list_triedy["chybajuci"] = chybajuci_uc
            return list_triedy

    def get_timetable(self):
        r = self.session.post(f"{self.edupage_address}timetable/server/currenttt.js?__func=curentttGetData",
                              data='{"__args":[null,{"year":2021,"datefrom":"2021-09-06","dateto":"2021-09-12","table":"classes","id":"562840","showColors":true,"showIgroupsInClasses":false,"showOrig":true}],"__gsh":"' + self.gsh + '"}')
        print(r.json()["r"]["ttitems"])
        # for period in r.json()["r"]["ttitems"]:
        #    print(f'hodina {period["uniperiod"]} {self.days[datetime.datetime.strptime(period["date"].replace("-", " "), "%Y %m %d").weekday()]} začína o {period["starttime"]} a končí o {period["endtime"]}')
        for period in r.json()["r"]["ttitems"]:
            print(
                f'{period["uniperiod"]}: {self.subjects[period["subjectid"]]["name"]} - {self.teachers[period["teacherids"][0]]["firstname"]} {self.teachers[period["teacherids"][0]]["lastname"]}')

    def get_id(self):
        r = self.session.post(f"{self.edupage_address}rpr/server/maindbi.js?__func=mainDBIAccessor",
                              data='{"__args":[null,2021,{"vt_filter":{"datefrom":"2021-09-16","dateto":"2021-09-22"}},{"op":"fetch","tables":[],"columns":[],"needed_part":{"teachers":["__name","cb_hidden","expired","firstname","lastname","short"],"classes":["__name","classroomid"],"classrooms":["__name","name","short"],"students":["__name","classid"],"subjects":["__name","name","short"]},"needed_combos":{},"client_filter":{},"info_tables":[],"info_columns":[]}],"__gsh":"' + self.gsh + '"}')
        self.teachers = {}
        for data in r.json()["r"]["tables"][0]["data_rows"]:
            self.teachers[data["id"]] = data
        self.subjects = {}
        for data in r.json()["r"]["tables"][1]["data_rows"]:
            self.subjects[data["id"]] = data
        # hardcoded anj and nej
        self.subjects["*2"] = {'id': '*2', 'name': 'anglický jazyk', 'short': 'ANJ', 'subname': ''}
        self.subjects["*3"] = {'id': '*3', 'name': 'nemecký jazyk', 'short': 'NEJ', 'subname': ''}


if __name__ == '__main__':
    login_data = load_pass("")
    edu = Edu("https://spspb.edupage.org/", login_data["username"], login_data["password"], enable_threading=False)
    edu.get_id()
    edu.get_timetable()
    pass
