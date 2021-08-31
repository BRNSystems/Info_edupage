import requests
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
"""r = requests.post("https://spspb.edupage.org/rpr/server/maindbi.js?__func=mainDBIAccessor", headers=headers, json={
    "__args": [None, 2021, {"vt_filter": {"datefrom": "2020-03-16", "dateto": "2020-06-22"}},
               {"op": "fetch", "tables": [], "columns": [],
                "needed_part": {"teachers": ["__name", "cb_hidden", "expired", "firstname", "lastname", "short"],
                                "classes": ["__name", "classroomid"], "classrooms": ["__name", "name", "short"],
                                "igroups": ["__name"], "students": ["__name", "classid"],
                                "subjects": ["__name", "name", "short"], "events": ["typ", "name"],
                                "event_types": ["name"], "subst_absents": ["date", "absent_typeid", "groupname"],
                                "periods": ["__name", "period", "starttime", "endtime"],
                                "dayparts": ["starttime", "endtime"], "dates": ["tt_num", "tt_day"]},
                "needed_combos": {}, "client_filter": {}, "info_tables": [], "info_columns": []}], "__gsh": "00000000"})"""
r = requests.post("https://spspb.edupage.org/timetable/server/currenttt.js?__func=curentttGetData", json={
    "__args": [None,
               {"year": 2021, "datefrom": "2019-03-01", "dateto": "2021-03-07", "table": "classrooms", "id": "vsetko",
                "showColors": True, "showIgroupsInClasses": False, "showOrig": True}], "__gsh": "00000000"})
print(r.text)
print(r.status_code)
with open("test.json", "w") as file:
    json.dump(r.json(), file, indent=2)
