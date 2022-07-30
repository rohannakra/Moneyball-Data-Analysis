
import pandas as pd
from plyer import notification
from sportsipy.mlb.teams import Teams

dataset = pd.read_csv('data management/data.csv')

dataset.drop(columns=['RankSeason', 'RankPlayoffs', 'OOBP', 'OSLG', 'RS', 'RA', 'W', 'G'], inplace=True)

# NOTE: We drop columns like OOBP because of null values.
#       We drop columns like W, RS, and RA because that would give away target.

dataset = dataset.iloc[::-1]    # Reversing dataset... so year increases w/index number

# Adding more data.
ERA = []
ERA_PLUS = []
FIP = []
HR = []
RBIs = []
Ks = []

notification.notify(
    title='Data preparation loading...',
    message=f'Estimated time until data is loaded: 27 min.',
    app_icon='jupyter_icon.ico'
)

for row in dataset.index:
    team = dataset.loc[row]['Team']
    year = dataset.loc[row]['Year']

    team_object = Teams(year)[team]
    
    ERA.append(team_object.earned_runs_against)
    ERA_PLUS.append(team_object.earned_runs_against_plus)
    FIP.append(team_object.fielding_independent_pitching)
    HR.append(team_object.home_runs)
    RBIs.append(team_object.runs_batted_in)
    Ks.append(team_object.strikeouts)


dataset['ERA'] = ERA
dataset['ERA+'] = ERA_PLUS
dataset['FIP'] = FIP
dataset['HR'] = HR
dataset['RBIs'] = RBIs
dataset['Ks'] = Ks

# Add samples from 2013-2021.
for year in range(2013, 2022):
    if year != 2020:
        for team in Teams(year)._teams:
            team_ = Teams(year)[team.abbreviation]    # This is the team object.
            
            if team_.rank >= 10:    # 10 teams make the playoffs every year (starting in 2022 it's 15 teams)
                playoff_label = 1
            else:
                playoff_label = 0

            sample = [
                team_.abbreviation, 
                'N/A', 
                year, 
                team_.on_base_percentage, 
                team_.slugging_percentage, 
                team_.batting_average, 
                playoff_label, 
                team_.earned_runs_against, 
                team_.earned_runs_against_plus, 
                team_.fielding_independent_pitching, 
                team_.home_runs, 
                team_.runs_batted_in, 
                team_.strikeouts
            ]
    
            dataset.loc[len(dataset.index)] = sample

# NOTE: We can put N/A for league because it won't be used for the model.

notification.notify(
    title='All data loaded',
    message=f"Data stored in file 'data_all.csv'",
    app_icon='jupyter_icon.ico'
)

dataset.to_csv('data management/data_all.csv')
