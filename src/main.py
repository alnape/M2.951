import pandas as pd
import time
from NBAscraper import NBA

scraper = NBA()

time_start = time.time()

team_data = scraper.getTeamLinks()
all_data = pd.DataFrame(columns=["TEAM", "NO", "NAME", "POS", "AGE", "HEIGHT", "WEIGHT", "COLLEGE", "SALARY"])
for i, row in enumerate(team_data.itertuples(), 1):
    print("Scraping data: "+ row.url_team)
    current_data = scraper.getPlayersTeam(row.url_team, row.name_team)
    all_data = pd.concat([all_data, current_data])
scraper.data2csv(all_data)

print("Process finished successfully!!! Time elapsed: {} seconds".format(time.time()-time_start))
