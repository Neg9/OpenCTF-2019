# Flip the Script  

## Score
64

## Description
Inject a single JavaScript payload in three contexts:
	unquoted, in a double-quoted string, and in a single-quoted string.

## Category
web

## Running in Docker
You can run the challenge with Docker.

    $ docker build .
    Successfully built <id>
    $ docker run -p 3000:3000 <id>

Then, access http://localhost:3000 in a browser.

## Running locally
If you don't want to use Docker, install NodeJS and run
`nodejs server.js`.

