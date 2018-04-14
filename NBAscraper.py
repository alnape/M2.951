class NBA():
    
    def __init__(self):
        self.home_page = "http://www.espn.com"
        #print(self.home_page)
        self.teams_page = "http://www.espn.com/nba/players"
        #print(self.teams_page)
        self.data = []
        #print(self.data)
        

    def data2csv(self, filename, data):
        # Overwrite to the specified file.
	    # Create it if does not exist.
        file = open(filename, "w+")
        data.to_csv(path_or_buf=file, sep=';', chunksize=1000, columns=["TEAM", "NO", "NAME", "POS", "AGE", "HEIGHT", "WEIGHT", "COLLEGE", "SALARY"])