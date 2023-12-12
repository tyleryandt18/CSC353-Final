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

CREATE TABLE off_player_stats (
    player_id INT,
    team_id INT,
    game_id VARCHAR(20),
    season VARCHAR(4),
    pos VARCHAR(4),
    rush_att INT,
    rush_yds INT,
    rush_tds INT, 
    pass_att INT,
    pass_cmps INT,
    pass_yds INT,
    pass_tds INT,
    ints INT,
    rec INT,
    rec_yds INT,
    rec_tds INT,
    fumbles INT,
    fumbles_lost INT,
    PRIMARY KEY(player_id, season, game_id),
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

CREATE TABLE def_player_stats (
    player_id INT,
    team_id INT,
    game_id VARCHAR(20),
    season VARCHAR(20),
    pos VARCHAR(4),
    fum_rec INT,
    fum_ret_tds INT,
    ints INT,
    int_ret_tds INT,
    safeties INT, 
    tackles_solo INT,
    tackles_assisted INT,
    tackles_forloss INT,
    sacks INT,
    qb_hurries INT,
    forced_fumbles INT, 
    pass_broken_up INT,
    PRIMARY KEY(player_id, season, game_id),
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

CREATE TABLE st_player_stats (
    player_id INT,
    team_id INT,
    game_id VARCHAR(20),
    season VARCHAR(4),
    pos VARCHAR(4),
    kickoff_ret INT,
    kickoff_ret_yds INT,
    kickoff_ret_tds INT,
    punt_ret INT,
    punt_ret_yds INT,
    punt_ret_tds INT,
    fg_att INT,
    fg_made INT,
    xp_att INT,
    xp_made INT,
    punts INT,
    punt_yds INT, 
    kickoffs INT,
    kickoff_touchbacks INT,
    kickoff_outofbounds INT,
    kicks_blocked INT,
    PRIMARY KEY(player_id, season, game_id),
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

CREATE TABLE team_stats (
    team_id INT,
    game_id VARCHAR(20),
    season VARCHAR(4),
    points_scored INT,
    time_of_possesion INT,
    penalties INT,
    penalty_yds INT,
    3rd_down_att INT,
    3rd_down_conv INT,
    4th_down_att INT,
    4th_down_conv INT,
    redzone_att INT,
    redzone_tds INT,
    redzone_fgs INT,
    PRIMARY KEY(team_id, season, game_id),
    -- FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
    
);