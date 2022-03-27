## Scrapes through player page and gets passing stats
import requests
import csv
from bs4 import BeautifulSoup

def get_player_bio(li_item):
    div_li = li_item.findAll("div", {"class": None})
    #div_li = div_li[1:len(div_li)]
    return ",".join([x.text for x in div_li])

## Player lookup is a table of player stats for a given year
player_lookup = {}
with open('instance/stats/players.csv') as fi:
    reader = csv.reader(fi)
    for row in reader:
        player_lookup[row[0]] = row

player_idx = []
with open('instance/stats/qb_player_idx.csv') as fi:
    reader = csv.reader(fi)
    for row in reader:
        player_idx.append(row)

#target_url = 'https://www.espn.com/nfl/player/gamelog/_/id/14881/russell-wilson'
target_url_base = 'https://www.espn.com/nfl/player/gamelog/_/id/'

for player in player_idx[1:len(player_idx)]:
    full_href = player[2]
    target_url_player = full_href.replace("http://www.espn.com/nfl/player/_/id/", "")
    print(target_url_player)
    target_url = target_url_base + target_url_player
    print(target_url)
    
    result = requests.get(target_url)
    raw_data = result.text
    # with open('test.html') as fi:
    #     raw_data = fi.read()
    pg = BeautifulSoup(raw_data, features='html.parser')

    ## Extract profile data
    ph_all = pg.findAll("div", {"class": "PlayerHeader__Container"})[0]
    name = ph_all.findAll("h1", {"class": "PlayerHeader__Name"})[0]
    name_str = " ".join([x.text for x in name.findAll("span")])
    team = ph_all.findAll("ul", {"class": "PlayerHeader__Team_Info"})[0]
    team_li = team.findAll("li")
    team_id = team_li[0]
    player_attr = {}
    player_attr['team'] = team_id.text
    try:
        player_attr['team_href'] = team_id.a['href']
    except TypeError:
        player_attr['team_href'] = None
    if len(team_li) > 1:
        player_attr['player_num'] = team_li[1].text
        player_attr['player_pos'] = team_li[2].text
    else:
        player_attr['player_num'] = None
        player_attr['player_pos'] = None
    player = ph_all.findAll("ul", {"class": "PlayerHeader__Bio_List"})[0]
    player_li = player.findAll("li")
    if len(player_li) > 4:
        player_attr['ht_wt'] = get_player_bio(player_li[0])
        player_attr['dob'] = get_player_bio(player_li[1])
        player_attr['college'] = get_player_bio(player_li[2])
        player_attr['draft_info'] = get_player_bio(player_li[3])
        player_attr['status'] = get_player_bio(player_li[4])
    else:
        player_attr['ht_wt'] = None
        player_attr['dob'] = None
        player_attr['college'] = None
        player_attr['draft_info'] = None
        player_attr['status'] = None

    print(player_attr)

    if target_url_player not in player_lookup.keys():
        with open('instance/stats/players.csv', 'a') as fi:
            output = [
                target_url_player,
                player_attr['team'],
                player_attr['team_href'],
                player_attr['player_num'],
                player_attr['player_pos'],
                player_attr['ht_wt'],
                player_attr['dob'],
                player_attr['college'],
                player_attr['draft_info'],
                player_attr['status']
            ]
            writer = csv.writer(fi)
            writer.writerow(output)
            player_lookup[target_url_player] = output

    ## Extract table data
    tbls = pg.findAll("table")
    tbl = tbls[0] ## Second one is a schedule table
    rows = tbl.findAll("tr")
    dataset = []
    for r, row in enumerate(rows):
        if r != 0:
            if r == 1:
                headers = []
                cols = row.findAll("th")
                for c, col in enumerate(cols):
                    headers.append(col.text)
            else:
                row_out = []
                cols = row.findAll("td")
                for c, col in enumerate(cols):
                    if c == 0 and col.text.startswith("Regular Season"):
                        break
                    row_out.append(col.text)
                if row_out != []:
                    dataset.append(row_out)
    with open('instance/stats/pass_stats.csv', 'a') as fi:
        writer = csv.writer(fi)
        for row in dataset:
            writer.writerow([target_url_player] + row)
    ## TODO: Need to actually write it so i extract data into a new table