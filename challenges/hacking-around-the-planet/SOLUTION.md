If you just try to go the the endpoint in a browser you will be redirected to a youtube video for "Around The World"
This is mostly for fun.

The endpoint sets a JWT cookie that contains a list of "places you've visited". 
The description says there must be another way to travel without planes (ie. actully going there)
This is the hint that you should be tricking the service.

The clue in the readme that its behind a proxy should lead you to X-Forwarded-For 
From there you need to submit ip addresses to get to 10.
