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

def filter_pos(pos):
    """
    A helper method that filters a position into one of the three respective classes.
    
    Parameters:
        - pos: the player's position
    
    Returns:
        the respective position class
    """

    if pos in ("RB", "QB", "WR", "TE", "OL", "FB"):
        return "OFF"
    elif pos in ("DB", "LB", "DL", "S"):
        return "DEF"
    elif pos in ("KR", "PR", "PK", "P", "K"):
        return "ST"
    else:
        return "NULL"

# Iterate over csv files
for folder in glob.glob("data/archive/cfbstats*"):
    season = folder.split("-")[2]
    files = os.listdir(folder)
    for file in files:
        if file == "conference.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue
                    
                    line = line.split(',')
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

        if file == "team.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')
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
        
        if file == "player.csv":
            first_line = True
            with open(folder + '/' + file, 'r') as f:
                for line in f:
                    if first_line:
                        first_line = False
                        continue

                    line = line.split(',')
                    player_id = line[0]
                    team_id = line[1]
                    first_name = line[3]
                    last_name = line[2]
                    number = line[4]
                    class_year = line[5]
                    position = line[6]
                    pos_class = filter_pos(position)

                    insert_query = "INSERT INTO players (id, first_name, last_name, season, team_id, pos, position_class, number, class) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    query_params = (player_id, first_name, last_name, season, team_id, position, pos_class, number, class_year)

                    try:
                        cursor.execute(insert_query, query_params)
                    except mysql.connector.Error as e:
                        print("Failed inserting tuple: {}".format(e))

connection.commit()
connection.close()