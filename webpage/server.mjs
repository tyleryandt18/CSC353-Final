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

app.get('/playerAttributes', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let playerName = request.query["player_name"]

    db.queryCallbackPlayer(playerName, (results) => {
        response.json(results)
    })
});

app.get('/tourney', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let date = request.query["date"]

    db.queryCallbackTourney(date, (results) => {
        response.json(results)
    })
});

app.get('/playerStats', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let player = request.query["player"]
    let start = request.query["start"]
    let end = request.query["end"]

    db.queryCallbackStats(player, start, end, (results) => {
        response.json(results)
    })
});

app.listen(port, () => console.log('Server is starting on PORT,', port))

process.on('exit', () => {
    db.disconnect()
})