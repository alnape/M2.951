import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class NBA():
    
    def __init__(self):
        self.url_home = "http://www.espn.com"
        self.url_teams = "http://www.espn.com/nba/players"
        self.output_file = "./Players_Season_2017_2018.csv"
        
    # Retorna un dataframe amb:
    #   columna1: links a les pagines dels equips
    #   columna2: nom de l'equip
    #def getTeamLinks(self, url_home, url_teams):
    def getTeamLinks(self):
        html_page = requests.get(self.url_teams)
        #team_data = ['http://www.espn.com/nba/teams/roster?team=UTAH']
        #Parsing a page with BeautifulSoup
        soup = BeautifulSoup(html_page.content, 'html.parser')
        #print([type(item) for item in list(soup.children)])
        teams = soup.find(id="my-players-table")

        links = [] 
        names = [] 
        for link in teams.findAll('a', attrs={'href': re.compile("roster")}):
            links.append(self.url_home + link.get('href').strip())        
            names.append(link.get_text().strip())
        
        data = pd.DataFrame({
            "url_team": links, 
            "name_team": names,
            })
        return data

    def getPlayersTeam(self, url_team, name_team):
        #print(url_team)
        html_page = requests.get(url_team)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        #soup = BeautifulSoup(open("C:\\table.html"), "html.parser")
        lst_players = []
        # Table that contains players
        tbl_players = soup.find_all('tr', {'class': re.compile('player')})

        for player in tbl_players:
            lst_players.append(player)

        #Attributes: TEAM, NO., NAME, POSITION, AGE, HEIGHT, WEIGHT, COLLEGE, 2017-2018 SALARY
        lst_team = []
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
            #TEAM
            lst_team.append(name_team)
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
            attr_sal = lst_players[i].find_all('td')[7].get_text().strip().replace('$','')
            lst_sals.append(attr_sal)
            i = i + 1

        data = pd.DataFrame({
            "TEAM": lst_team,
            "NO": lst_nos, 
            "NAME": lst_names, 
            "POS": lst_pos, 
            "AGE":lst_ages,
            "HEIGHT":lst_hts,
            "WEIGHT":lst_wts,
            "COLLEGE":lst_cols,
            "SALARY":lst_sals
        })
        return data

    def data2csv(self, all_data):
        # Create it if does not exist / Overwrite to the specified file.
        file = open(self.output_file, "w+")
        all_data.to_csv(path_or_buf=file, sep=';', index=False, chunksize=1000, columns=["TEAM", "NO", "NAME", "POS", "AGE", "HEIGHT", "WEIGHT", "COLLEGE", "SALARY"])