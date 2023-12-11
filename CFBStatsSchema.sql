-- SQLBook: Code
DROP Schema if EXISTS cfbStats;
CREATE Schema cfbStats;
USE cfbStats;
CREATE TABLE conferences (
    id INT,
    name VARCHAR(30),
    subdivision VARCHAR(5),
    PRIMARY KEY (id)
);
CREATE TABLE teams (
    id INT,
    name VARCHAR(30), 
    conference_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (conference_id) REFERENCES conferences(id) ON DELETE SET NULL
);
CREATE TABLE players (
    id INT,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    season VARCHAR(4),
    team_id INT,
    pos VARCHAR(4),
    position_class VARCHAR(4),
    number VARCHAR(20),
    class VARCHAR(2),
    PRIMARY KEY(id, season),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);

CREATE TABLE games (
    id  VARCHAR(20),
    winner_id INT,
    loser_id INT,
    winner_score VARCHAR(3),
    loser_score VARCHAR(3),
    home_id INT,
    away_id INT,
    season VARCHAR(4),
    PRIMARY KEY(id, season),
    FOREIGN KEY (winner_id) REFERENCES teams(id) ON DELETE SET NULL,
    FOREIGN KEY (loser_id) REFERENCES teams(id) ON DELETE SET NULL,
    FOREIGN KEY (home_id) REFERENCES teams(id) ON DELETE SET NULL,
    FOREIGN KEY (away_id) REFERENCES teams(id) ON DELETE SET NULL
);

-- CREATE TABLE off_player_stats (
--     player_id
--     season
--     pos
--     rush_att
--     rush_yds
--     rush_tds
--     pass_att
--     pass_cmps
--     pass_yds
--     pass_tds
--     pass_ints
--     pass_conv
--     rec
--     rec_yds
--     rec_tds
--     fumbles
--     fumbles_lost
--     PRIMARY KEY(player_id, season)
-- );

-- CREATE TABLE def_player_stats (
--     player_id
--     season
--     pos
--     fum_rec
--     fum_ret_yds
--     fum_ret_tds
--     interceptions
--     int_ret_yds
--     int_ret_tds
--     safeties
--     tackles_solo
--     tackles_assisted
--     tackles_forloss
--     sacks
--     qb_hurries
--     forced_fumbles
--     pass_broken_up
--     PRIMARY KEY(player_id, season)
-- );

-- CREATE TABLE st_player_stats (
--     player_id
--     season
--     pos
--     kickoff_ret
--     kickoff_ret_yds
--     kickoff_ret_tds
--     punt_ret
--     punt_ret_yds
--     punt_ret_tds
--     fg_att
--     fg_made
--     xp_att
--     xp_made
--     punts
--     punt_yds
--     kickoffs
--     kickoff_yds
--     kickoff_touchbacks
--     kickoff_outofbounds
--     onside_kicks
--     kicks_blocked
--     PRIMARY KEY(player_id, season)
-- );

-- CREATE TABLE team_stats (
--     team_id
--     season
--     ...
--     PRIMARY KEY(team_id, season)
-- );