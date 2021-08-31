import json
import time
import requests
test_lenght_substitution = 7
url_school = "https://spspb.edupage.org/"
account = {"username": "JakubDuris", "password": "TKNENLAAEU"}


def get_substitutions():
    substitutions = edupage.post(url_school + "substitution/server/viewer.js?__func=getSubstViewerDayDataHtml",
                                 data='{"__args":[null,{"date":"2021-06-22","mode":"classes"}],"__gsh": "' + gsh + '"}')
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
            if len(line) < test_lenght_substitution:
                try:
                    int(line)
                except:
                    if "(" and ")" not in line:
                        trieda = line
                        list_triedy[line] = {}
            if trieda == None:
                raise LookupError("Invalid substitution data")
            if len(line) > test_lenght_substitution and line != "celý deň":
                if line == '<img src="/global/pics/ui/absent_32.svg" style="height:16px;display:inline-block;vertical-align:text-bottom;margin-right:5px"/>Chýba':
                    list_triedy[trieda][list_parsed[position - 1]] = "Chýba"
                else:
                    list_triedy[trieda][list_parsed[position-1]] = line
        list_triedy["chybajuci"] = chybajuci_uc
        return list_triedy


try:
    url = 'https://spspb.edupage.org/login/edubarLogin.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
    # values = {'username': f"{accounts[account]['name']}",
    #          'password': f"{weird_shuffle(accounts[account]['password'])}"}
    edupage = requests.session()
    edupage.post(url, data=account, headers=headers)
    r = edupage.get("https://spspb.edupage.org/timeline/", headers=headers)
    x = r.text.split("\n")
    gsh = x[59].split('"')[1]
    print(get_substitutions())
except EOFError as e:
    time.sleep(0.5)
    print(str(e))
