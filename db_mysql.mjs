// You have to do an 'npm install mysql2' to get the package
// Documentation in: https://www.npmjs.com/package/mysql2

import { createConnection } from 'mysql2';

var connection = createConnection({
	host: 'localhost',
	user: 'root',
	password: 'catsAREw1ld!',
	database: 'cfbStats'
});

function connect() {
	connection.connect();
}

function getTeamFromConference(conference, callback) {
	connection.query("SELECT teams.name FROM teams, conferences WHERE teams.conference_id = conferences.id AND conferences.name = ? ORDER BY name", [conference], (error, results, fields) => {
		if (error) throw error;

		callback(results);
	})
}

function getPlayerFromTeam(team, season, pos, callback) {
	connection.query("SELECT DISTINCT CONCAT(players.first_name, ' ', players.last_name) AS name FROM teams, players WHERE teams.id = players.team_id AND teams.name = ? AND players.season = ? AND players.position_class = ? ORDER BY name", [team, season, pos], (error, results, fields) => {
		if (error) throw error;

		callback(results);
	})
}

function getPlayerStats(season, player, pos, callback) {
	let table = '';
	if(pos == "OFF"){
		table = "off_player_stats";
	} else if (pos == "DEF"){
		table = "def_player_stats";
	} else {
		table = "st_player_stats";
	}

	const query = "SELECT DISTINCT CONCAT(p.first_name, ' ', p.last_name) as name, tb.* FROM " + table + " as tb JOIN players p ON tb.player_id = p.id WHERE CONCAT(p.first_name, ' ', p.last_name) = ? AND tb.season = ?";
	connection.query(query, [player, season], (error, results, fields) => {
		if (error) throw error;
		
		callback(results);
	})
}

function disconnect() {
	connection.end();
}

// Setup exports to include the external variables/functions
export {
	connection,
	connect,
	disconnect,
	getTeamFromConference,
	getPlayerFromTeam,
	getPlayerStats
}

// For testing:
//connect()
//queryCallbackStats("Kei Nishikori", "2018-01-20", "2020-01-20", r => console.log(r))
//queryCallbackPlayer("Kei Nishikori", r => console.log(r))
//disconnect()