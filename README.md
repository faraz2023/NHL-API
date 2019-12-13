# NHL-RESTful API

# User Stories

#### 1. Game Results Summary

As a **casual** fan I like to be able to see the brief results (Who won, how many goals) of games from any given date so I better understand what is going on in the league.

#### 2. Game Results Details

As a **stats junkie** I like to see the performance details of both teams in a given game so I know better how my favorite teams are doing in the league.

#### 3. Game Player Stats

As a **fantasy hockey player** I like to be able to see the performance of each player in both team at a given game so I know how best arrange my fantasy team.

---

# Acceptance Criteria

#### 1. Game Results Summary

- Ability to specify the desired date
- Ability to list all the games that had occur in the give date.
- For each game provide:
  - The abbreviation of the home team
  - The abbreviation of the away team
  - The number of goals from the home team
  - The number of goals from the away team
  - Who won the game

#### 2. Game Results Details

- The ability to specify the desired game.
- The ability to list the teams involved in the given game
- Provide the venue of the game
- The exact time of the game
- For each team involved in the game provide:
  - The abbreviation of the home and away team
  - The number of shots
  - The number of hits
  - The penalty minutes

#### 3. Game Player Stats

- The ability to specify the desired game.
- The ability to list the teams that played the game
- The ability to provide the venue of the game
- The ability to list all the players involved in the game and provide the information:
  - Time on ice
  - Shots
  - Goals
  - Assists
  - Firs name and last name
  - Birth place and birth date
  - Nationality

##

## API Documentation

No authentication needed to request data from this API.

#

#### Retrieve Matches by Date

```
GET /api/results?date={YYYY-MM-DD}
```

| Parameter | Type     | Description                                    |
| :-------- | :------- | :--------------------------------------------- |
| `date`    | `string` | **Required**. Valid date in format: YYYY-MM-DD |

### Response

JSON representation of games that played on specified `date`. However, if an invalid request is submitted, or some
other error occurs, API returns an HTML response with relevant status code specifying the problem.

```
TEST /api/results?date=2012-05-03
```

```javascript
{
    "games": [
        {
            "away_team": {
                "abbreviation": "PHI",
                "franchiseId": 16,
                "shortName": "Philadelphia",
                "teamName": "Flyers",
                "team_id": 4
            },
            "game_data": {
                "away_goals": 3,
                "date_time": "2012-05-03",
                "date_time_GMT": "2012-05-03T23:30:00Z",
                "game_id": 2011030223,
                "home_goals": 4,
                "home_rink_side_start": "left",
                "outcome": "home win OT",
                "season": 20112012,
                "title": "PHI vs NJD",
                "type": "P",
                "venue": "Prudential Center",
                "venue_time_zone_id": "America/New_York"
            },
            "home_team": {
                "abbreviation": "NJD",
                "franchiseId": 23,
                "shortName": "New Jersey",
                "teamName": "Devils",
                "team_id": 1
            },
            "players_detail_uri": "/api/results/2011030223/players",
            "teams_detail_uri": "/api/results/2011030223/teams"
        }
    ]
}
```

#### Return Data

| Attribute              | Type      | Description                                                                             |
| :--------------------- | :-------- | :-------------------------------------------------------------------------------------- |
| `games`                | `array`   | Array of `game` JSON objects                                                            |
| `away_team`            | `object`  | JSON representation of away `team` object                                               |
| `game_data`            | `object`  | JSON representation of information for a specific game                                  |
| `home_team`            | `object`  | JSON representation of home `team` object                                               |
| `players_details_uri`  | `string`  | Link to API to request information on players for this game                             |
| `teams_details_uri`    | `string`  | Link to API to request information on teams for this game                               |
| `abbreviation`         | `string`  | Representation team's name abbreviated                                                  |
| `franchiseID`          | `integer` | ID of the franchise team belongs to                                                     |
| `team_id`              | `integer` | Unique ID of the team                                                                   |
| `shortName`            | `string`  | Short representation team's name (typically a city the team plays for)                  |
| `teamName`             | `string`  | Representation of the team's name                                                       |
| `title`                | `string`  | Title of `game` showing teams that played each other                                    |
| `away_goals`           | `integer` | Final goal count for away team                                                          |
| `home_goals`           | `integer` | Final goal count for home team                                                          |
| `date_time`            | `string`  | Representation of date game was played. Format: YYYY-MM-DD                              |
| `date_time_GMT`        | `string`  | Representation of date and time game was played in GMT time                             |
| `game_id`              | `integer` | Unique ID of the game                                                                   |
| `home_rink_side_start` | `string`  | Side that home team starts the game                                                     |
| `outcome`              | `string`  | Describes outcome of the game and if it finished in overtime (OT) or regular time (REG) |
| `type`                 | `string`  | Type of game played. 'P' == Playoff ; 'R' == Regular                                    |
| `season`               | `integer` | Unique ID of the season being played                                                    |
| `venue`                | `string`  | Name of the location the game is being played                                           |
| `venue_time_zone_id`   | `string`  | Timezone of the location where the game is being played                                 |

##

#### Game's team information

```
GET /api/results/{ game_id }/teams
```

| Parameter | Type      | Description                                                  |
| :-------- | :-------- | :----------------------------------------------------------- |
| `game_id` | `integer` | **Required**. Unique id for the game data is being requested |

### Response

JSON representation of stats for the teams that played in specified `game_id`. Includes relevant information of
game data for quick access. However, if an invalid request is submitted, or some
other error occurs, API returns an HTML response with relevant status code specifying the problem.

```
TEST /api/results/2011030223/teams
```

```javascript
{
    "away_team": {
        "abbreviation": "PHI",
        "faceOffWinPercentage": 50.8,
        "franchiseId": 16,
        "giveaways": 2,
        "goals": 3,
        "head_coach": "Peter Laviolette",
        "hits": 28,
        "pim": 4,
        "powerPlayGoals": 1,
        "powerPlayOpportunities": 5,
        "settled_in": "OT",
        "shortName": "Philadelphia",
        "shots": 28,
        "takeaways": 1,
        "teamName": "Flyers",
        "team_id": 4,
        "won": false
    },
    "game_data": {
        "date_time": "2012-05-03",
        "home_rink_side_start": "left",
        "type": "P",
        "venue": "Prudential Center"
    },
    "home_team": {
        "abbreviation": "NJD",
        "faceOffWinPercentage": 49.2,
        "franchiseId": 23,
        "giveaways": 11,
        "goals": 4,
        "head_coach": "Peter DeBoer",
        "hits": 30,
        "pim": 10,
        "powerPlayGoals": 1,
        "powerPlayOpportunities": 2,
        "settled_in": "OT",
        "shortName": "New Jersey",
        "shots": 31,
        "takeaways": 4,
        "teamName": "Devils",
        "team_id": 1,
        "won": true
    },
    "players_detail_uri": "/api/results/2011030223/players"
}
```

#### Return Data

| Attribute                | Type      | Description                                                                    |
| :----------------------- | :-------- | :----------------------------------------------------------------------------- |
| `away_team`              | `object`  | JSON representation of away `team` information and statistics                  |
| `game_data`              | `object`  | Information about specified game                                               |
| `home_team`              | `object`  | JSON representation of home `team` information and statistics                  |
| `players_details_uri`    | `string`  | Link to API to request information on players for this game                    |
| `abbreviation`           | `string`  | Representation team's name abbreviated                                         |
| `franchiseID`            | `integer` | ID of the franchise team belongs to                                            |
| `team_id`                | `integer` | Unique ID of the team                                                          |
| `shortName`              | `string`  | Short representation team's name (typically a city the team plays for)         |
| `teamName`               | `string`  | Representation of the team's name                                              |
| `goals`                  | `integer` | Final goal count for the team                                                  |
| `faceOffWinPercentage`   | `float`   | Percentage of face off wins in the game                                        |
| `giveaways`              | `integer` | Number of times puck was given away by this team in the game                   |
| `hits`                   | `integer` | Number of hits taken by this team in the game                                  |
| `pim`                    | `integer` | Penalties in minutes during this game                                          |
| `powerPlayGoals`         | `integer` | Number of goals during a power play                                            |
| `powerPlayOpportunities` | `integer` | Number of power plays opportunities the team has during the game               |
| `shots`                  | `integer` | Number of shots taken by the team                                              |
| `takeaways`              | `integer` | Number of times the team's players took back possession of the puck            |
| `won`                    | `boolean` | Indicates if team won the game                                                 |
| `head_coach`             | `string`  | First and Last name of the head coach of the team                              |
| `date_time`              | `string`  | Representation of date game was played. Format: YYYY-MM-DD                     |
| `home_rink_side_start`   | `string`  | Side that home team starts the game                                            |
| `settled_in`             | `string`  | Representation of when the game ended. 'OT' == Overtime; 'REG' == Regular time |
| `type`                   | `string`  | Type of game played. 'P' == Playoff ; 'R' == Regular                           |
| `venue`                  | `string`  | Name of the location the game is being played                                  |

##

#### Game's player information

```
GET /api/results/{ game_id }/players
```

| Parameter | Type      | Description                                                  |
| :-------- | :-------- | :----------------------------------------------------------- |
| `game_id` | `integer` | **Required**. Unique id for the game data is being requested |

### Response

JSON representation of game stats for the players that played in specified `game_id`. However, if an invalid request is
submitted, or some other error occurs, API returns an HTML response with relevant status code specifying the problem.

```
TEST /api/results/2011030223/players
```

```javascript
{
    "away_team_players": {
        "goalies": [
            {
                "assists": 0,
                "birthCity": "Togliatti",
                "birthDate": "1980-06-22",
                "decision": "L",
                "evenSaves": 25,
                "evenShotsAgainst": 28,
                "evenStrengthSavePercentage": 89.2857142857143,
                "firstName": "Ilya",
                "goals": 0,
                "lastName": "Bryzgalov",
                "nationality": "RUS",
                "pim": 0,
                "player_detail_uri": "/api/players/8468524",
                "player_id": 8468524,
                "powerPlaySavePercentage": 50,
                "powerPlaySaves": 1,
                "powerPlayShotsAgainst": 2,
                "primaryPosition": "G",
                "savePercentage": 87.09677419354841,
                "saves": 27,
                "shortHandedSaves": 1,
                "shortHandedShotsAgainst": 1,
                "shots": 31,
                "team_id": 4,
                "timeOnIce": 4623
            }
        ],
        "skaters": [
            {
                "assists": 1,
                "birthCity": "Regina",
                "birthDate": "1982-04-18",
                "blocked": 2,
                "evenTimeOnIce": 986,
                "faceOffWins": 3,
                "faceoffTaken": 5,
                "firstName": "Scott",
                "giveaways": 0,
                "goals": 0,
                "hits": 4,
                "lastName": "Hartnell",
                "nationality": "CAN",
                "penaltyMinutes": 0,
                "player_detail_uri": "/api/players/8468486",
                "player_id": 8468486,
                "plusMinus": -2,
                "powerPlayAssists": 0,
                "powerPlayGoals": 0,
                "powerPlayTimeOnIce": 339,
                "primaryPosition": "LW",
                "shortHandedAssists": 0,
                "shortHandedGoals": 0,
                "shortHandedTimeOnIce": 0,
                "shots": 3,
                "takeaways": 0,
                "team_id": 4,
                "timeOnIce": 1325
            }, ...
        ]
    },
    "home_team_players": {
        "goalies": [
            {
                "assists": 0,
                "birthCity": "Montreal",
                "birthDate": "1972-05-06",
                "decision": "W",
                "evenSaves": 21,
                "evenShotsAgainst": 23,
                "evenStrengthSavePercentage": 91.304347826087,
                "firstName": "Martin",
                "goals": 0,
                "lastName": "Brodeur",
                "nationality": "CAN",
                "pim": 0,
                "player_detail_uri": "/api/players/8455710",
                "player_id": 8455710,
                "powerPlaySavePercentage": 80,
                "powerPlaySaves": 4,
                "powerPlayShotsAgainst": 5,
                "primaryPosition": "G",
                "savePercentage": 89.2857142857143,
                "saves": 25,
                "shortHandedSaves": 0,
                "shortHandedShotsAgainst": 0,
                "shots": 28,
                "team_id": 1,
                "timeOnIce": 4641
            }
        ],
        "skaters": [
            {
                "assists": 1,
                "birthCity": "Kiev",
                "birthDate": "1980-04-09",
                "blocked": 0,
                "evenTimeOnIce": 1023,
                "faceOffWins": 1,
                "faceoffTaken": 1,
                "firstName": "Alexei",
                "giveaways": 0,
                "goals": 1,
                "hits": 3,
                "lastName": "Ponikarovsky",
                "nationality": "UKR",
                "penaltyMinutes": 0,
                "player_detail_uri": "/api/players/8467412",
                "player_id": 8467412,
                "plusMinus": 1,
                "powerPlayAssists": 0,
                "powerPlayGoals": 0,
                "powerPlayTimeOnIce": 0,
                "primaryPosition": "LW",
                "shortHandedAssists": 0,
                "shortHandedGoals": 0,
                "shortHandedTimeOnIce": 68,
                "shots": 4,
                "takeaways": 0,
                "team_id": 1,
                "timeOnIce": 1091
            }, ...
        ]
    },
    "teams_detail_uri": "/api/results/2011030223/teams"
}
```

#### Return Data

| Attribute                    | Type      | Description                                                         |
| :--------------------------- | :-------- | :------------------------------------------------------------------ |
| `away_team_players`          | `object`  | JSON representation of away `team` goalies and skaters              |
| `home_team_players`          | `object`  | JSON representation of home `team` goalies and skaters              |
| `teams_details_uri`          | `string`  | Link to API to request information on teams for this game           |
| `goalies`                    | `array`   | Array of goalies played for the team in the game                    |
| `skaters`                    | `array`   | Array of skaters played for the team in the game                    |
| `player_details_uri`         | `string`  | Link to API to request information on player                        |
| `assists`                    | `integer` | Number of assists in the game                                       |
| `birthCity`                  | `string`  | City where player was born                                          |
| `birthDate`                  | `string`  | Player's date of birth                                              |
| `blocked`                    | `integer` | Number of times players was blocked                                 |
| `decision`                   | `string`  | Support neutral win or loss returns 'W' or 'L' respectively         |
| `evenSaves`                  | `integer` | Number of even saves in the game                                    |
| `evenShotsAgainst`           | `integer` | Number of even shot against                                         |
| `evenStrengthSavePercentage` | `float`   | Percentage representing strength save                               |
| `evenTimeOnIce`              | `integer` | Even time on ice in seconds                                         |
| `team_id`                    | `integer` | Unique ID of the team                                               |
| `firstName`                  | `string`  | Player's first name                                                 |
| `lastName`                   | `string`  | Player's last name                                                  |
| `goals`                      | `integer` | Final goal count for player in the game                             |
| `player_id`                  | `integer` | Unique ID of the player                                             |
| `nationality`                | `string`  | Player's nationality (abbreviation)                                 |
| `powerPlaySavePercentage`    | `float`   | Percentage of saves made during a power play                        |
| `powerPlaySaves`             | `integer` | Number of saves during power play                                   |
| `powerPlayShotsAgainst`      | `integer` | Number of shots taken on during power play                          |
| `primaryPosition`            | `string`  | Players primary position                                            |
| `savePercentage`             | `float`   | Percentage of saves made the game                                   |
| `saves`                      | `integer` | Total number of saves made during the game                          |
| `shortHandedSaves`           | `integer` | Number of short handed saves                                        |
| `shortHandedSavesAgainst`    | `integer` | Number of short handed saves against                                |
| `timeOnIce`                  | `integer` | Time spend on ice in seconds                                        |
| `faceOffWins`                | `integer` | Number of wins during face off                                      |
| `faceOffTaken`               | `integer` | Total number of face offs taken during the game                     |
| `giveaways`                  | `integer` | Number of times puck was given away by this team in the game        |
| `hits`                       | `integer` | Number of hits taken by this team in the game                       |
| `penaltyMinutes`             | `integer` | Penalties in minutes during this game                               |
| `plusMinus`                  | `integer` | Plus or Minus points in the game                                    |
| `powerPlayAssists`           | `integer` | Number of assists during a power play                               |
| `powerPlayGoals`             | `integer` | Number of goals during a power play                                 |
| `powerPlayTimeOnIce`         | `integer` | Number of seconds spent on ice during power plays                   |
| `shortHandedAssists`         | `integer` | Number of assists during short handed play                          |
| `shortHandedGoals`           | `integer` | Number of goals during short handed play                            |
| `shortHandedTimeOnIce`       | `integer` | Number of seconds spent on ice during short handed plays            |
| `shots`                      | `integer` | Number of shots taken by the team                                   |
| `takeaways`                  | `integer` | Number of times the team's players took back possession of the puck |

##

#### Game's score information/timeline

```
GET /api/results/{ game_id }/scoringsummary
```

| Parameter | Type      | Description                                                  |
| :-------- | :-------- | :----------------------------------------------------------- |
| `game_id` | `integer` | **Required**. Unique id for the game data is being requested |

### Response

JSON representation of goals scored during the specified `game_id` and the information associated with it.
Goals are returned in chronological order. However, if an invalid request is
submitted, or some other error occurs, API returns an HTML response with relevant status code specifying the problem.

```
TEST /api/results/2011030223/scoringsummary
```

```javascript
{
    "goal_timeline": [
        {
            "away_score": 1,
            "game_time": "06:08",
            "home_score": 0,
            "period": 1,
            "period_time": "06:08",
            "scorer": {
                "assists": [
                    {
                        "firstName": "Daniel",
                        "lastName": "Briere",
                        "player_detail_uri": "/api/players/8464975",
                        "player_id": 8464975
                    },
                    {
                        "firstName": "Jaromir",
                        "lastName": "Jagr",
                        "player_detail_uri": "/api/players/8448208",
                        "player_id": 8448208
                    }
                ],
                "firstName": "Brayden",
                "goals": 1,
                "lastName": "Schenn",
                "player_detail_uri": "/api/players/8475170",
                "player_id": 8475170
            }
        }, ...
    ],
    "players_details_uri": "/api/results/2011030223/players",
    "teams_details_uri": "/api/results/2011030223/teams"
}
```

#### Return Data

| Attribute             | Type      | Description                                                                                       |
| :-------------------- | :-------- | :------------------------------------------------------------------------------------------------ |
| `teams_details_uri`   | `string`  | Link to API to request information on teams for this game                                         |
| `players_details_uri` | `string`  | Link to API to request information on players in this game                                        |
| `goal_timeline`       | `array`   | Array of goal objects for goals scored during the game                                            |
| `away_score`          | `integer` | Current number of goals for away team at time `game_time`                                         |
| `game_time`           | `string`  | Representation of the overall time (not period specific) the goal was in the game in MM:SS format |
| `home_score`          | `integer` | Current number of goals for home team at time `game_time`                                         |
| `period`              | `integer` | Number represents the period in which the goal was scored. `period >= 4` represents overtime      |
| `period_time`         | `string`  | Representation of the time the goal was scored in the period in MM:SS format                      |
| `scorer`              | `object`  | JSON representation of the scorer information                                                     |
| `assists`             | `array`   | Array of players that assisted in scoring the goal                                                |
| `firstName`           | `string`  | Player's first name                                                                               |
| `lastName`            | `string`  | Player's last name                                                                                |
| `player_details_uri`  | `string`  | Link to API to request information on player                                                      |
| `player_id`           | `integer` | Unique ID of the player                                                                           |
| `goals`               | `integer` | (Current) number of goals the scorer has made in the game at time `game_time`                     |
| `season_goals`        | `integer` | Number of goals the scorer has made in the season at time `game_time`                             |
