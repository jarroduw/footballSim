## Scrapes through player page and gets passing stats
import requests
import csv
from bs4 import BeautifulSoup

#target_url = 'https://www.espn.com/nfl/stats/player/_/view/offense/table/passing/sort/passingYards/dir/desc'
target_url = 'https://www.espn.com/nfl/stats/player/_/view/offense/stat/rushing'
target_url = 'https://www.espn.com/nfl/stats/player/_/view/special/stat/punting'

## Download page

result = requests.get(target_url)
data = result.text
# with open('test_player_idx.html', 'w') as fi:
#     fi.write(result.text)

#with open('test_player_idx.html') as fi:
#    data = fi.read()

## Parse page
soup = BeautifulSoup(data, features='html.parser')
tbls = soup.findAll("table")
## First table is the player info
## Second table is the stats    
player_rows = tbls[0].findAll('tr')
stat_rows = tbls[1].findAll('tr')
if len(player_rows) != len(stat_rows):
    raise AttributeError("PLayer rows and stat rows not the same")

headers_player = []
players = []
headers_stat = []
stats = []
for p, player_row in enumerate(player_rows):
    stat_row = stat_rows[p]
    if p == 0:
        for c in player_row.findAll("th"):
            headers_player.append(c.text)
        headers_player.append("player_href")
        headers_player.append("team")
        for c in stat_row.findAll("th"):
            headers_stat.append(c.text)
    else:
        temp = []
        for i, c in enumerate(player_row.findAll("td")):
            if i == 1:
                href = c.a['href']
                text = c.a.text
                team = c.find("span").text
                temp.append(text)
                temp.append(href)
                temp.append(team)
            else:
                temp.append(c.text)
        players.append(temp)
        temp = []
        for c in stat_row.findAll("td"):
            temp.append(c.text)
        stats.append(temp)

## Create/Check records for each player in a player index

with open("instance/stats/punt_player_idx.csv", "w") as fi:
    writer = csv.writer(fi)
    writer.writerow(headers_player + headers_stat)
    for r, row in enumerate(players):
        writer.writerow(row + stats[r])