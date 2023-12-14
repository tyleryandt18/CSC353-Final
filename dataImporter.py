"""
A program that populates a mySQL database with college football statistics.
Statistics downloaded from: https://www.kaggle.com/datasets/mhixon/college-football-statistics/

Authors: John Matsudaira, Parker McNamara, Tyler Yandt
"""

import mysql.connector
import glob
import os

# Create the mySQL connection
connection = mysql.connector.connect(user='root', password='catsAREw1ld!', host='localhost')
cursor = connection.cursor()
databaseName = "CSC353FinalDB"
with open ("CFBStatsSchema.sql", 'r') as f:
    schema_string = f.read()

# Drop the database if it exists
try:
    cursor.execute("DROP DATABASE IF EXISTS {}".format(databaseName))
except mysql.connector.Error as error_descriptor:
    print("Failed dropping database: {}".format(error_descriptor))
    exit(1)

# Create database
try:
    cursor.execute("CREATE DATABASE {}".format(databaseName))
except mysql.connector.Error as error_descriptor:
    print("Failed creating database: {}".format(error_descriptor))
    exit(1)

# Use the database
try:
    cursor.execute("USE {}".format(databaseName))
except mysql.connector.Error as error_descriptor:
    print("Failed using database: {}".format(error_descriptor))
    exit(1)

# Execute the SQL schema
try:
    for result in cursor.execute(schema_string, multi=True):
        pass
except mysql.connector.Error as error_descriptor:
    if error_descriptor.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table already exists: {}".format(error_descriptor))
    else:
        print("Failed creating schema: {}".format(error_descriptor))
    exit(1)
cursor.close()

# Reopen the cursor
cursor = connection.cursor()

# Keep track of seen data entries
teams = {}
conferences = {}
team_stats = {}

def filter_pos(pos):
    """
    A helper method that filters a position into one of the three respective classes.
    
    Parameters:
        - pos: the player's position
    
    Returns:
        the respective position class
    """

    if pos in ("RB", "QB", "WR", "TE", "OL", "OG", "OT", "C", "FB", "TB", "SE", "FL", "SB", "HB"):
        return "OFF"
    elif pos in ("DB", "LB", "DL", "S", "CB", "OLB", "DE", "DT", "FS", "ILB", "NT", "SS", "WLB", "NG", "DS", "SLB", "MLB", "ROV", "RV"):
        return "DEF"
    elif pos in ("KR", "PR", "PK", "P", "K", "LS", "HOLD"):
        return "ST"
    elif pos == "ATH":
        return "ALL"
    else:
        return None

# Iterate over csv files
for folder in glob.glob("data/archive/cfbstats*"):
    files = os.listdir(folder)

    season = folder.split("-")[2]
    games = {} # reset the game for each new season (each new set of files)
    players = {} # same for players

    file_order = ["conference.csv", "team.csv", "team-game-statistics.csv", "game.csv",
                  "player.csv", "player-game-statistics.csv"]

    for file in file_order:
        if file == "conference.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue
                    
                    line = line.split(',')

                    i = 0
                    for value in line:
                        line[i] = value.replace('"', '') # clean csv formatting
                        if value == '':
                            line[i] = None
                        i += 1
                    
                    conference_id = line[0]
                    conference_name = line[1]
                    subdivison = line[2]

                    if conference_id not in conferences:
                        conferences[conference_id] = conference_name
                        insert_query = "INSERT INTO conferences (id, name, subdivision) VALUES (%s, %s, %s)"
                        query_params = (conference_id, conference_name, subdivison)

                        try:
                            cursor.execute(insert_query, query_params)
                        except mysql.connector.Error as e:
                            print("Failed inserting tuple: {}".format(e))

        elif file == "team.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')

                    i = 0
                    for value in line:
                        line[i] = value.strip('"') # clean csv formatting
                        if value == '':
                            line[i] = None
                        i += 1
                    
                    team_id = line[0]
                    team_name = line[1]
                    conference_id = line[2]

                    if team_id not in teams:
                        teams[team_id] = team_name
                        insert_query = "INSERT INTO teams (id, name, conference_id) VALUES (%s, %s, %s)"
                        query_params = (team_id, team_name, conference_id)

                        try:
                            cursor.execute(insert_query, query_params)
                        except mysql.connector.Error as e:
                            print("Failed inserting tuple: {}".format(e))

        elif file == "team-game-statistics.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')

                    i = 0
                    for value in line:
                        line[i] = value.strip('"') # clean csv formatting
                        if value == '':
                            line[i] = None
                        i += 1

                    game_id = line[1]
                    team_id = line[0]
                    top = line[-10]
                    penalties = line[-9]
                    penalty_yds = line[-8]
                    third_att = line[-7]
                    third_conv = line[-6]
                    fourth_att = line[-5]
                    fourth_conv = line[-4]
                    rz_att = line[-3]
                    rz_td = line[-2]
                    rz_fg = line[-1]
                    team_score = line[35]

                    if game_id not in games:
                        games[game_id] = [[team_id, team_score]]
                    elif len(games[game_id]) == 1:
                        # Put the higher score first, therefore the winner is always first in the data structure
                        if int(team_score) > int(games[game_id][0][1]):
                            games[game_id].insert(0, [team_id, team_score])
                        else:
                            games[game_id].append([team_id, team_score])

                    query_params = (team_id, game_id, season, team_score, top, penalties, penalty_yds,
                                    third_att, third_conv, fourth_att, fourth_conv, rz_att, rz_td, rz_fg)

                    # save query information for later because we need to populate the games entity before tema_stats
                    team_stats[(team_id, game_id)] = query_params
    
        elif file == "player.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')

                    i = 0
                    for value in line:
                        line[i] = value.strip('"') # clean csv formatting
                        if value == '':
                            line[i] = None
                        i += 1

                    player_id = line[0]
                    team_id = line[1]
                    first_name = line[3]
                    last_name = line[2]
                    number = line[4]
                    class_year = line[5]
                    position = line[6]

                    if first_name == 'Team' or last_name == 'Team':
                        continue

                    # Handling csv formatting issues
                    try:
                        number = int(number)
                    except:
                        if number is not None:
                            test = number[0]
                            try:
                                test = int(test)
                            except:
                                first_name = number
                                last_name = last_name + first_name
                                number = line[5]
                                class_year = line[6]
                                position = line[7]

                    pos_class = filter_pos(position)
                    
                    if player_id not in players:
                        players[player_id] = [team_id, position]

                    insert_query = "INSERT INTO players (id, first_name, last_name, season, team_id, pos, position_class, number, class) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    query_params = (player_id, first_name, last_name, season, team_id, position, pos_class, number, class_year)

                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))

        elif file == "game.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')

                    i = 0
                    for value in line:
                        line[i] = value.strip('"') # clean csv formatting
                        if value == '':
                            line[i] = None
                        i += 1
                
                    game_id = line[0]
                    try:
                        winner_id = games[game_id][0][0]
                        loser_id = games[game_id][1][0]
                        winner_score = games[game_id][0][1]
                        loser_score = games[game_id][1][1]
                    except Exception:
                        print("Game {} not found.".format(game_id))
                        winner_id, loser_id, winner_score, loser_score = None

                    home_id = line[3]
                    away_id = line[2]

                    insert_query = "INSERT INTO games (id, winner_id, loser_id, winner_score, loser_score, home_id, away_id, season) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    query_params = (game_id, winner_id, loser_id, winner_score, loser_score, home_id, away_id, season)

                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))

                    # Enter team stats
                    insert_query = """INSERT INTO team_stats
                    (team_id, game_id, season, points_scored, time_of_possesion, penalties, penalty_yds,
                    3rd_down_att, 3rd_down_conv, 4th_down_att, 4th_down_conv, redzone_att, redzone_tds, redzone_fgs) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    query_params = team_stats[(home_id, game_id)]
                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))
                    query_params = team_stats[(away_id, game_id)]
                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))
                    


        elif file == "player-game-statistics.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')

                    i = 0
                    for value in line:
                        line[i] = value.strip('"') # clean csv formatting
                        if value == '':
                            line[i] = None
                        i += 1

                     # general info
                    player_id = line[0]
                    try:
                        team_id = players[player_id][0]
                        pos = players[player_id][1]
                    except KeyError:
                        # player doesn't exist in the player.csv file, therefore we skip them
                        continue
                    game_id = line[1]

                    # Offense stats
                    rush_att = line[2]
                    rush_yds = line[3]
                    rush_tds = line[4]
                    pass_att = line[5]
                    pass_comp = line[6]
                    pass_yds = line[7]
                    pass_tds = line[8]
                    pass_int = line[9]
                    rec = line[11]
                    rec_yds = line[12]
                    rec_tds = line[13]
                    fumbles = line[46]
                    fumbles_lost = line[47]

                    # Defense stat
                    fum_rec = line[20]
                    fum_ret_tds = line[22]
                    interceptions = line[23]
                    int_tds = line[25]
                    safeties = line[37]
                    solo_tackles = line[48]
                    assisted_tackles = line[49]
                    tackles_for_loss = line[50]
                    sacks = line[52]
                    qb_hurries = line[54]
                    forced_fumbles = line[55]
                    pass_broken = line[56]

                    # Special Teams stats
                    kickoff_ret = line[14]
                    kickoff_ret_yds = line[15]
                    kickoff_ret_tds = line[16]
                    punt_ret = line[17]
                    punt_ret_yds = line[18]
                    punt_ret_tds = line[19]
                    fg_att = line[29]
                    fg_made = line[30]
                    xp_att = line[31]
                    xp_made = line[32]
                    punts = line[39]
                    punt_yds = line[40]
                    kickoffs = line[41]
                    kickoff_touchbacks = line[43]
                    kickoff_outofbounds = line[44]
                    kicks_blocked = line[-1]

                    insert_query = """INSERT INTO off_player_stats (
                        player_id, team_id, game_id, season, pos, rush_att, rush_yds, rush_tds,
                        pass_att, pass_cmps, pass_yds, pass_tds, ints, rec, rec_yds, rec_tds, fumbles, fumbles_lost
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    query_params = (
                        player_id, team_id, game_id, season, pos, rush_att, rush_yds, rush_tds,
                        pass_att, pass_comp, pass_yds, pass_tds, pass_int, rec, rec_yds, rec_tds, fumbles, fumbles_lost
                    )
                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))
                    
                    insert_query = """INSERT INTO def_player_stats (
                        player_id, team_id, game_id, season, pos, fum_rec, fum_ret_tds, ints,
                        int_ret_tds, safeties, tackles_solo, tackles_assisted, tackles_forloss, sacks, qb_hurries,
                        forced_fumbles, pass_broken_up
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    query_params = (
                        player_id, team_id, game_id, season, pos, fum_rec, fum_ret_tds, interceptions,
                        int_tds, safeties, solo_tackles, assisted_tackles, tackles_for_loss, sacks, qb_hurries,
                        forced_fumbles, pass_broken
                    )
                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))

                    insert_query = """INSERT INTO st_player_stats (
                        player_id, team_id, game_id, season, pos, kickoff_ret, kickoff_ret_yds, kickoff_ret_tds,
                        punt_ret, punt_ret_yds, punt_ret_tds, fg_att, fg_made, xp_att, xp_made, punts, punt_yds, kickoffs,
                        kickoff_touchbacks, kickoff_outofbounds, kicks_blocked
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    query_params = (
                        player_id, team_id, game_id, season, pos, kickoff_ret, kickoff_ret_yds, kickoff_ret_tds,
                        punt_ret, punt_ret_yds, punt_ret_tds, fg_att, fg_made, xp_att, xp_made, punts, punt_yds, kickoffs,
                        kickoff_touchbacks, kickoff_outofbounds, kicks_blocked
                    )
                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))

connection.commit()
connection.close()