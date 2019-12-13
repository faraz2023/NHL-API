from flask import Flask, jsonify, abort, request, render_template
import pandas as pd
import numpy as np
from helper import validate_date
import time
import re

app = Flask(__name__)


# importing the data
def load_teams_data():
    td = pd.read_csv("./team_info.csv")
    return td


def load_game_data():
    gd = pd.read_csv("./game.csv")
    return gd


def load_game_goalie_stats():
    game_goalie_stat = pd.read_csv("./game_goalie_stats.csv")
    return game_goalie_stat


def load_game_plays():
    game_play = pd.read_csv("./game_plays.csv")
    return game_play


def load_game_plays_players():
    game_plays_player = pd.read_csv("./game_plays_players.csv")
    return game_plays_player


def load_game_teams_stats():
    game_teams_stat = pd.read_csv("./game_teams_stats.csv")
    return game_teams_stat


def load_game_shifts():
    game_shift = pd.read_csv("./game_shifts.csv")
    return game_shift


def load_game_skater_stats():
    game_skater_stat = pd.read_csv("./game_skater_stats.csv")
    return game_skater_stat


def load_player_info():
    player_information = pd.read_csv("./player_info.csv")
    return player_information


# global variables
team_data = load_teams_data()
print("successfully loaded teams data")
game_data = load_game_data()
print("successfully loaded games data")
game_goalie_stats = load_game_goalie_stats()
print("successfully loaded game goalie stats")
game_plays = load_game_plays()
print("successfully loaded game plays")
game_plays_players = load_game_plays_players()
print("successfully loaded game plays players")
game_shifts = load_game_shifts()
print("successfully loaded game shifts")
game_skater_stats = load_game_skater_stats()
print("successfully loaded game skater stats")
game_teams_stats = load_game_teams_stats()
print("successfully loaded game teams stats")
player_info = load_player_info()
print("successfully loaded player info")


@app.route('/')
def index():
    return "NHL API"


# Route mapping for HTTP GET on /api/results 
# Retrieves game summary information
@app.route('/api/results', methods=['GET'])
def game_results_summary():
    try:
        date_string = request.args.get('date')

        # Check for date
        if not date_string:
            return render_template('404.html', error="Date Missing", message="Date must be provided \
            in the following format: date={YYYY-MM-DD}"), 404

        # Verify that date is correct format
        if not validate_date(date_string):
            return render_template('404.html', error="Date Invalid", message="Date is not valid. Date must be valid \
            calendar date with the following format: date={YYYY-MM-DD}"), 404

        games = game_data[game_data["date_time"] == date_string]

        # Return 404 if there isn't any game on the given date
        if games.shape[0] < 1:
            return render_template('404.html', error="No Resource Found", message="No games found on this date"), 404

        games_array = []
        for i, row in games.iterrows():
            game_id = row['game_id']

            away_team = team_data[team_data['team_id'] == row['away_team_id']]
            away_team = away_team.loc[:, away_team.columns != 'link'].to_dict('records')[0]

            home_team = team_data[team_data['team_id'] == row['home_team_id']]
            home_team = home_team.loc[:, home_team.columns != 'link'].to_dict('records')[0]

            game_info = row.drop(['home_team_id', 'away_team_id', 'venue_link', 'venue_time_zone_offset',
                                  'venue_time_zone_tz'], axis=0)

            game_info['title'] = away_team['abbreviation'] + ' vs ' + home_team['abbreviation']

            dict_game = {'teams_detail_uri': "/api/results/" + str(game_id) + "/teams",
                         'players_detail_uri': "/api/results/" + str(game_id) + "/players",
                         'game_data': game_info.to_dict(),
                         'away_team': away_team,
                         'home_team': home_team}

            games_array.append(dict_game)

        games_dict = {"games": games_array}
        return jsonify(games_dict)
    except Exception as error:
        return render_template('500.html', error=error), 500


# Route mapping for HTTP GET on /api/results/{ID}/teams
# Retrieves a game's detailed information on teams
@app.route('/api/results/<int:game_id>/teams', methods=['GET'])
def game_results_details(game_id):
    try:
        # Retrieving the game
        df_game = game_data[game_data["game_id"] == game_id]

        # Check if the game_id actually exists in the data set
        if df_game.shape[0] < 1:
            return render_template('404.html', error="No Resource Found", message="No game found with id \
            " + str(game_id) + ". Please double check game_id"), 404

        # Retrieving the away and home teams
        away_team = team_data[team_data["team_id"] == df_game.iloc[0]["away_team_id"]]
        home_team = team_data[team_data["team_id"] == df_game.iloc[0]["home_team_id"]]

        # Retrieving team's game stat
        teams_stats = game_teams_stats[game_teams_stats["game_id"] == game_id]

        # Remove irrelevant and redundant data
        away_team_stats = teams_stats.merge(away_team, on="team_id")
        # Move settled in to game information
        settled = away_team_stats[['settled_in']]
        away_team_stats = away_team_stats.drop(['settled_in', 'HoA', 'link', 'game_id'], axis=1)

        home_team_stats = teams_stats.merge(home_team, on="team_id")
        home_team_stats = home_team_stats.drop(['settled_in', 'HoA', 'link', 'game_id'], axis=1)

        # Only some additional information for game data as this route is more for team stats
        game_info = df_game[['date_time', 'home_rink_side_start', 'type', 'venue']]
        game_info['settled_in'] = settled.iloc[0]['settled_in']

        dict_game = {'players_detail_uri': "/api/results/" + str(game_id) + "/players",
                     'game_data': game_info.to_dict('records')[0],
                     'away_team': away_team_stats.to_dict('records')[0],
                     'home_team': home_team_stats.to_dict('records')[0]}

        return jsonify(dict_game)
    except Exception as error:
        return render_template('500.html', error=error), 500


# Route mapping for HTTP GET on /api/results/{ID}/players
# Retrieves a game's detailed information on players
@app.route('/api/results/<int:game_id>/players', methods=['GET'])
def game_players_details(game_id):
    try:
        # Retrieving the game
        df_game = game_data[game_data["game_id"] == game_id]

        # Check if the game_id actually exists in the data set
        if df_game.shape[0] < 1:
            return render_template('404.html', error="No Resource Found", message="No game found with id \
                    " + str(game_id) + ". Please double check game_id"), 404

        # Retrieving the team IDs
        away_team_id = df_game.iloc[0]['away_team_id']
        home_team_id = df_game.iloc[0]['home_team_id']

        # Retrieving all the players in the game and add player detail uri
        current_game_skaters = \
            game_skater_stats[game_skater_stats['game_id'] == game_id].merge(player_info, on="player_id")
        for i, row in current_game_skaters.iterrows():
            current_game_skaters.at[i, 'player_detail_uri'] = "/api/players/" + str(
                current_game_skaters.at[i, 'player_id'])

        current_game_goalies = \
            game_goalie_stats[game_goalie_stats['game_id'] == game_id].merge(player_info, on="player_id")
        for i, row in current_game_goalies.iterrows():
            current_game_goalies.at[i, 'player_detail_uri'] = "/api/players/" + str(
                current_game_goalies.at[i, 'player_id'])

        # The away team dictionary
        away_goalies = current_game_goalies[current_game_goalies['team_id'] == away_team_id]
        away_goalies = away_goalies.drop(['game_id', 'link'], axis=1)

        away_skaters = current_game_skaters[current_game_skaters['team_id'] == away_team_id]
        away_skaters = away_skaters.drop(['game_id', 'link'], axis=1)

        away_team_dict = {
            'skaters': away_skaters.to_dict('records'),
            'goalies': away_goalies.to_dict('records')}

        # The home team dictionary
        home_goalies = current_game_goalies[current_game_goalies['team_id'] == home_team_id]
        home_goalies = home_goalies.drop(['game_id', 'link'], axis=1)

        home_skaters = current_game_skaters[current_game_skaters['team_id'] == home_team_id]
        home_skaters = home_skaters.drop(['game_id', 'link'], axis=1)

        home_team_dict = {
            'skaters': home_skaters.to_dict('records'),
            'goalies': home_goalies.to_dict('records')}

        # link to game_details resource
        # Filling in the game_player_details
        game_players_detail = {'teams_detail_uri': "/api/results/" + str(game_id) + "/teams",
                               'away_team_players': away_team_dict,
                               'home_team_players': home_team_dict}

        return jsonify(game_players_detail)
    except Exception as error:
        return render_template('500.html', error=error), 500


# ENHANCEMENTS
# Route mapping for HTTP GET on /api/results/{ID}/scoringsummary 
# Retrieves a game's detailed goals information
@app.route('/api/results/<int:game_id>/scoringsummary', methods=['GET'])
def game_goals_details(game_id):
    try:
        # Retrieving the game
        game = game_data[game_data["game_id"] == game_id]

        # Check if the game_id actually exists in the data set
        if game.shape[0] < 1:
            return render_template('404.html', error="No Resource Found", message="No game found with id \
                            " + str(game_id) + ". Please double check game_id"), 404

        # Making the hyperlinks for the other resources
        goals_return_obj = {'teams_details_uri': "/api/results/" + str(game_id) + "/teams",
                            'players_details_uri': "/api/results/" + str(game_id) + "/players"}

        # Retrieving the desired game's goals
        current_game_plays = game_plays[game_plays['game_id'] == game_id]
        current_game_goals = current_game_plays[current_game_plays['event'] == "Goal"]

        # A list to populate with goals' info
        goals_list = []

        game_scorers = {}

        # Iterating over the goals
        for j, row in current_game_goals.iterrows():

            # the dictionary of this specific goal
            goal_dict = {}

            # Retrieving all the players involved with the goal
            goal_players = game_plays_players[game_plays_players['play_id'] == row['play_id']]
            goal_players = goal_players.merge(player_info, on='player_id')

            # Removing redundant and unnecessary data
            goal_players = goal_players.drop(['game_id', 'link', 'play_id'], axis=1)

            # Adding the hyperlinks for all the players involved in the goal to the data
            goal_players['player_detail_uri'] = ''
            for i, r in goal_players.iterrows():
                goal_players.at[i, 'player_detail_uri'] = "/api/players/" + str(goal_players.at[i, 'player_id'])

            # Differentiating between the scorer and the assist(s)
            scorer = goal_players[goal_players['playerType'] == "Scorer"]
            scorer = scorer[['firstName', 'lastName', 'player_id', 'player_detail_uri']]

            assists = goal_players[goal_players['playerType'] == "Assist"]
            assists = assists[['firstName', 'lastName', 'player_id', 'player_detail_uri']]

            # Populating this goal dictionary
            goal_dict['scorer'] = scorer.to_dict('records')[0]
            goal_dict['scorer']['assists'] = assists.to_dict('records')

            # Assumes description always lists scorer first
            goal_dict['scorer']['season_goals'] = \
                int(re.compile(r"\((\d+)\)").findall(row['description'].split(',')[0])[0])

            goal_dict['away_score'] = row['goals_away']
            goal_dict['home_score'] = row['goals_home']
            goal_seconds = ((row['period'] - 1) * 1200) + (row['periodTime'])
            goal_dict['period_time'] = time.strftime('%M:%S', time.gmtime(row['periodTime']))
            goal_dict['period'] = row['period']
            goal_dict['seconds'] = goal_seconds
            hours = goal_seconds // 3600

            # Add 60 minutes to minutes to maintain MM:SS format if goal is in 4th period (overtime)
            if hours > 0:
                minutes = (goal_seconds % 3600) // 60
                seconds = goal_seconds % 60
                seconds_str = '0' + str(seconds) if seconds < 10 else str(seconds)
                minutes_str = str(minutes + 60)
                goal_dict['game_time'] = minutes_str + ":" + seconds_str
            else:
                goal_dict['game_time'] = time.strftime('%M:%S', time.gmtime(goal_seconds))

            # Retrieving the number of goals made by the scorer so far in the game
            if goal_dict['scorer']['player_id'] in game_scorers:
                game_scorers[goal_dict['scorer']['player_id']] += 1
            else:
                game_scorers[goal_dict['scorer']['player_id']] = 1
            goal_dict['scorer']['goals'] = game_scorers[goal_dict['scorer']['player_id']]

            # Adding this goal to the list of goals
            goals_list.append(goal_dict)

        # Putting the list of goals in the returned dictionary
        goals_return_obj['goal_timeline'] = sorted(goals_list, key=lambda x: x['seconds'])

        # Remove seconds after sorting
        for d in goals_return_obj['goal_timeline']:
            del d['seconds']

        return jsonify(goals_return_obj)
    except Exception as error:
        return render_template('500.html', error=error), 500


# Route mapping for HTTP GET on /api/teams/TOR
@app.route('/api/teams/<string:team_id>', methods=['GET'])
def get_task(team_id):
    # Fetch sub dataframe for all teams (hopefully 1) where abbreviation=team_id
    teams = team_data[team_data["abbreviation"] == team_id]

    # return 404 if there isn't one team
    if teams.shape[0] < 1:
        abort(404)

    # get first team
    team = teams.iloc[0]

    # return customized JSON structure in lieu of Pandas Dataframe to_json method
    teamJSON = {"abbreviation": team["abbreviation"],
                "city": team["shortName"],
                "name": team["teamName"]}

    # jsonify easly converts maps to JSON strings
    return jsonify(teamJSON)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error="Page Not Found", message="Please check the URL Requested"), 404


if __name__ == '__main__':
    app.run(debug=True)
