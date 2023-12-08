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

# Keep track of seen teams
teams = {}

# Iterate over csv files
for folder in glob.glob("data/archive/cfbstats*"):
    files = os.listdir(folder)
    for file in files:
        if file == "team.csv":
            with open(file, 'r') as f:
                for line in f:
