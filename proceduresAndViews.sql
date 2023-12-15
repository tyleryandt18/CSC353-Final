USE cfbStats;

DROP FUNCTION IF EXISTS avgRushYds;

DELIMITER //
CREATE FUNCTION avgRushYds(firstn VARCHAR(20), lastn VARCHAR(20), team VARCHAR(20), season VARCHAR(4)) RETURNS FLOAT(4,2) READS SQL DATA
BEGIN
	DECLARE avg_rush_yds FLOAT(4,2);

	SELECT AVG(rush_yds) INTO avg_rush_yds FROM off_player_stats, teams, players
	WHERE players.id = off_player_stats.player_id
	AND players.first_name = firstn
	AND players.last_name = lastn
	AND players.team_id = teams.id 
	AND teams.name = team
	AND off_player_stats.season = season;
		
	RETURN avg_rush_yds;
	
END
//

DROP FUNCTION IF EXISTS avgPassYds;

DELIMITER //
CREATE FUNCTION avgPassYds(firstn VARCHAR(20), lastn VARCHAR(20), team VARCHAR(20), season VARCHAR(4)) RETURNS FLOAT(4,2) READS SQL DATA
BEGIN
	DECLARE avg_pass_yds FLOAT(4,2);

	SELECT AVG(pass_yds) INTO avg_pass_yds FROM off_player_stats, teams, players
	WHERE players.id = off_player_stats.player_id
	AND players.first_name = firstn
	AND players.last_name = lastn
	AND players.team_id = teams.id 
	AND teams.name = team
	AND off_player_stats.season = season;
		
	RETURN avg_pass_yds;
	
END
//

DROP FUNCTION IF EXISTS avgRecYds;

DELIMITER //
CREATE FUNCTION avgRecYds(firstn VARCHAR(20), lastn VARCHAR(20), team VARCHAR(20), season VARCHAR(4)) RETURNS FLOAT(4,2) READS SQL DATA
BEGIN
	DECLARE avg_rec_yds FLOAT(4,2);

	SELECT AVG(rec_yds) INTO avg_rec_yds FROM off_player_stats, teams, players
	WHERE players.id = off_player_stats.player_id
	AND players.first_name = firstn
	AND players.last_name = lastn
	AND players.team_id = teams.id 
	AND teams.name = team
	AND off_player_stats.season = season;
		
	RETURN avg_rec_yds;
	
END
//

DROP FUNCTION IF EXISTS avgPassYds;

DELIMITER //
CREATE FUNCTION avgInts(firstn VARCHAR(20), lastn VARCHAR(20), team VARCHAR(20), season VARCHAR(4)) RETURNS FLOAT(4,2) READS SQL DATA
BEGIN
	DECLARE avg_ints FLOAT(4,2);

	SELECT AVG(ints) INTO avg_ints FROM def_player_stats, teams, players
	WHERE players.id = def_player_stats.player_id
	AND players.first_name = firstn
	AND players.last_name = lastn
	AND players.team_id = teams.id 
	AND teams.name = team
	AND def_player_stats.season = season;
		
	RETURN avg_ints;
	
END
//

DROP VIEW IF EXISTS top_season_passer_ratings;

CREATE VIEW top_season_passer_ratings AS
SELECT DISTINCT
    p.id,
    p.first_name,
    p.last_name,
    p.team_id,
    ops.season,
    (
        (
            (CASE
                WHEN (CAST(total_pass_cmps AS FLOAT) / total_pass_att - 0.3) * 5 < 0 THEN 0
                WHEN (CAST(total_pass_cmps AS FLOAT) / total_pass_att - 0.3) * 5 > 2.375 THEN 2.375
                ELSE (CAST(total_pass_cmps AS FLOAT) / total_pass_att - 0.3) * 5
            END) +
            (CASE
                WHEN (CAST(total_pass_yds AS FLOAT) / total_pass_att - 3) * 0.25 < 0 THEN 0
                WHEN (CAST(total_pass_yds AS FLOAT) / total_pass_att - 3) * 0.25 > 2.375 THEN 2.375
                ELSE (CAST(total_pass_yds AS FLOAT) / total_pass_att - 3) * 0.25
            END) +
            (CASE
                WHEN (CAST(total_pass_tds AS FLOAT) / total_pass_att) * 20 < 0 THEN 0
                WHEN (CAST(total_pass_tds AS FLOAT) / total_pass_att) * 20 > 2.375 THEN 2.375
                ELSE (CAST(total_pass_tds AS FLOAT) / total_pass_att) * 20
            END) +
            (CASE
                WHEN 2.375 - (CAST(total_pass_ints AS FLOAT) / total_pass_att) * 25 < 0 THEN 0
                WHEN 2.375 - (CAST(total_pass_ints AS FLOAT) / total_pass_att) * 25 > 2.375 THEN 2.375
                ELSE 2.375 - (CAST(total_pass_ints AS FLOAT) / total_pass_att) * 25
            END)
        ) / 6 * 100
    ) AS passer_rating
FROM
    players p
INNER JOIN (
    SELECT
        player_id,
        season,
        SUM(pass_att) AS total_pass_att,
        SUM(pass_cmps) AS total_pass_cmps,
        SUM(pass_yds) AS total_pass_yds,
        SUM(pass_tds) AS total_pass_tds,
        SUM(ints) AS total_pass_ints
    FROM
        off_player_stats
    GROUP BY
        player_id, season
) ops ON p.id = ops.player_id
WHERE
    ops.total_pass_att > 100
ORDER BY
    ops.season, passer_rating DESC;
