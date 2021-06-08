import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# 東京 23 区
# base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&pc=50"

# 福岡県
base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=090&bs=040&ra=040&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&rn=6015&rn=7020&rn=7050&rn=7035&rn=7025&rn=7015&rn=7145&rn=7055&rn=7040&rn=7045&rn=7170&rn=7310&rn=7155&rn=7280&rn=7285&rn=7290&rn=7215&rn=7065&rn=7070&rn=7060&rn=7005&rn=7085&rn=7295&rn=7575&rn=7135"

all_data = ["名称", "カテゴリー", "アドレス", "アクセス", "築年数", "構造", "階数", "家賃", "管理費", "敷金", "礼金", "間取り", "面積", "URL"]
max_page = 10

f = open('output.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

writer.writerow(["名称", "カテゴリー", "アドレス", "アクセス", "築年数", "構造", "階数", "家賃", "管理費", "敷金", "礼金", "間取り", "面積", "URL"])

for page in range(1, max_page + 1):

    url = base_url.format(page)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    items = soup.findAll("div", {"class": "cassetteitem"})
    print("page", page, "items", len(items))

    for item in items:
        stations = item.findAll("div", {"class": "cassetteitem_detail-text"})

        for station in stations:
            base_data = {}

            base_data["名称"] = item.find("div", {"class": "cassetteitem_content-title"}).getText().strip()
            base_data["カテゴリー"] = item.find("div", {"class": "cassetteitem_content-label"}).getText().strip()
            base_data["アドレス"] = item.find("li", {"class": "cassetteitem_detail-col1"}).getText().strip()
            base_data["アクセス"] = station.getText().strip()
            base_data["築年数"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip()
            base_data["構造"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[1].getText().strip()

            tbodys = item.find("table", {"class": "cassetteitem_other"}).findAll("tbody")

            for tbody in tbodys:
                data = base_data.copy()

                data["階数"] = tbody.findAll("td")[2].getText().strip()
                data["家賃"] = tbody.findAll("td")[3].findAll("li")[0].getText().strip()
                data["管理費"] = tbody.findAll("td")[3].findAll("li")[1].getText().strip()
                data["敷金"] = tbody.findAll("td")[4].findAll("li")[0].getText().strip()
                data["礼金"] = tbody.findAll("td")[4].findAll("li")[1].getText().strip()
                data["間取り"] = tbody.findAll("td")[5].findAll("li")[0].getText().strip()
                data["面積"] = tbody.findAll("td")[5].findAll("li")[1].getText().strip()
                data["URL"] = "https://suumo.jp" + tbody.findAll("td")[8].find("a").get("href")

                all_data.append(data)

                writer.writerow([
                    base_data["名称"],
                    base_data["カテゴリー"],
                    base_data["アドレス"],
                    base_data["アクセス"],
                    base_data["築年数"],
                    base_data["構造"],
                    data["階数"],
                    data["家賃"],
                    data["管理費"],
                    data["敷金"],
                    data["礼金"],
                    data["間取り"],
                    data["面積"],
                    data["URL"]
                ])

df = pd.DataFrame(all_data)

f.close()
