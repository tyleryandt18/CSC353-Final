// This is a framework to handle server-side content

// You have to do an 'npm install express' to get the package
// Documentation in: https://expressjs.com/en/starter/hello-world.html
import express from 'express';

import * as db from "./db_mysql.mjs";

var app = express();
let port = 3001

db.connect();

// Serve static HTML files in the current directory (called '.')
app.use(express.static('.'))

// For GET requests to "/student?field1=value1&field2=value2"

app.get('/getTeam', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let conferenceName = request.query["conference_name"]

    db.getTeamFromConference(conferenceName, (results) => {
        response.json(results)
    })
});

app.get('/getPlayer', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let teamName = request.query["team_name"]
    let season = request.query["season"]
    let pos = request.query["pos_class"]

    db.getPlayerFromTeam(teamName, season, pos, (results) => {
        response.json(results)
    })
});

app.get('/getPlayerStats', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let season = request.query["season"]
    let player = request.query["player_name"]
    let pos = request.query["pos_class"]

    db.getPlayerStats(season, player, pos, (results) => {
        response.json(results)
    })
});

app.listen(port, () => console.log('Server is starting on PORT,', port))

process.on('exit', () => {
    db.disconnect()
})