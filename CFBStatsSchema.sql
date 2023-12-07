DROP Schema if EXISTS cfbStats;
CREATE Schema cfbStats;
USE cfbStats;

CREATE TABLE players (
    id
    name
    season
    team
    pos
    position_class
    number
    class
);

CREATE TABLE teams (
    id
    name
    conference_id
);

CREATE TABLE conferences (
    id
    name
);

CREATE TABLE games (
    id
    winner_id
    loser_id
    home_id
    away_id
    season
);

CREATE TABLE off_player_stats (
    player_id
    season
    pos
    ...
);

CREATE TABLE def_player_stats (
    player_id
    season
    pos
    ...
);

CREATE TABLE st_player_stats (
    player_id
    season
    pos
    ...
);

CREATE TABLE team_stats (
    team_id
    season
    ...
);