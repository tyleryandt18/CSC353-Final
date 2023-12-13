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

function queryCallbackPlayer(playerName, callback) {
	connection.query("SELECT * FROM players WHERE player_name = ?", [playerName], (error, results, fields) => {
		if (error) throw error;

		console.log(results)
		callback(results);
	});

	// With parameters:
	// "... WHERE name = ?", ['Fernanda'], (error ...)
}

function queryCallbackTourney(date, callback) {
	connection.query("SELECT * FROM tournaments WHERE tournament_id LIKE ?", [date + '%'], (error, results, fields) => {
		if (error) throw error;

		console.log(results)
		callback(results);
	});
}

function queryCallbackStats(player, start, end, callback) {
	connection.query("call ShowAggregateStatistic(?, ?, ?)", [player, start, end], (error, results, fields) => {
		if (error) throw error;

		console.log(results)
		callback(results);
	});

}

function disconnect() {
	connection.end();
}

// Setup exports to include the external variables/functions
export {
	connection,
	connect,
	queryCallbackPlayer,
	queryCallbackTourney,
	queryCallbackStats,
	disconnect
}

// For testing:
//connect()
//queryCallbackStats("Kei Nishikori", "2018-01-20", "2020-01-20", r => console.log(r))
//queryCallbackPlayer("Kei Nishikori", r => console.log(r))
//disconnect()