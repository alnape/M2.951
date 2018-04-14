import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from NBAscraper import NBA

home_page = "http://www.espn.com"
teams_page = "http://www.espn.com/nba/players"

scraper = NBA()

def getTeamLinks(url_home, url_teams):
    html_page = requests.get(url_teams)
    #Parsing a page with BeautifulSoup
    soup = BeautifulSoup(html_page.content, 'html.parser')
    #print([type(item) for item in list(soup.children)])
    teams = soup.find(id="my-players-table")

    links = [] 
    for link in teams.findAll('a', attrs={'href': re.compile("roster")}):
        links.append(url_home + link.get('href'))
 
    return links

def getPlayersTeam(url_team):
    html_page = requests.get(url_team)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    players = soup.find('div', class_="mod-container mod-table mod-no-header-footer")
    links = [] 
    for link in players.findAll('a', attrs={'href': re.compile("player")}):
        #links.append(link.get('href'))
        links.append(link.get_text())
    
    return links

def scrap_table(url_team):
    print(url_team)
    html_page = requests.get(url_team)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    #print(soup.prettify())
    #f = open('workfile', 'w')
    #f.write(soup.prettify())
    # Only oddrow and evenrow
    lista = []
    for table_row in soup.select('tablehead tr[class*="row"]'):
    #for table_row in soup.select('tablehead tr'):        
        lista.append(table_row)
        print(table_row) #.get_text())
    return lista

#team_links = getTeamLinks(home_page, teams_page)
#print(team_links[0])
#players_team = getPlayersTeam(team_links[0])
#print(players_team)

#mytable = scrap_table(team_links[0])
#mytable = scrap_table(team_links[0])
soup = BeautifulSoup(open("C:\\table.html"), "html.parser")
#print(soup.prettify())
lst_players = []
# Table that contains players
tbl_players = soup.find_all('tr', {'class': re.compile('player')})

for player in tbl_players:
    lst_players.append(player)

#Attributes: NO., NAME, POSITION, AGE, HEIGHT, WEIGHT, COLLEGE, 2017-2018 SALARY
lst_nos = []
lst_names = []
lst_pos = []
lst_ages = []    
lst_hts = []    
lst_wts = []    
lst_cols = []
lst_sals = []
i = 0    
while (i < len(lst_players)):    
    #NO.    
    attr_no = lst_players[i].find_all('td')[0].get_text().strip()  
    lst_nos.append(attr_no)  
    #NAME
    attr_name = lst_players[i].find_all('td')[1].get_text().strip() 
    lst_names.append(attr_name)  
    #POS
    attr_pos = lst_players[i].find_all('td')[2].get_text().strip()
    lst_pos.append(attr_pos)
    #AGE
    attr_age = lst_players[i].find_all('td')[3].get_text().strip()
    lst_ages.append(attr_age)
    #HT
    attr_ht = lst_players[i].find_all('td')[4].get_text().strip()
    lst_hts.append(attr_ht)
    #WT
    attr_wt = lst_players[i].find_all('td')[5].get_text().strip()
    lst_wts.append(attr_wt)
    #COLLEGE
    attr_col = lst_players[i].find_all('td')[6].get_text().strip()
    lst_cols.append(attr_col)
    #2017-2018 SALARY
    attr_sal = lst_players[i].find_all('td')[7].get_text().strip()
    lst_sals.append(attr_sal)
    i = i + 1

data = pd.DataFrame({
        "NO": lst_nos, 
        "NAME": lst_names, 
        "POS": lst_pos, 
        "AGE":lst_ages,
        "HEIGHT":lst_hts,
        "WEIGHT":lst_wts,
        "COLLEGE":lst_cols,
        "2017-2018 SALARY":lst_sals
    })
print(data)

output_file = "dataset.csv"
scraper.data2csv(output_file, data)

#self.data.append(lst_names)
#scraper.scrape();
#scraper.data2csv(output_file)

#f = open('players.html', 'w')
#rows=tabla.findAll("tr")
#print(lista)

#for i in range(len(team_links)):
#    print("scraping crash data: "+ team_links[i])

#f = open('players.html', 'w')
#f.write(tabla.prettify())
