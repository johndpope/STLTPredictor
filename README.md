# STLTPredictor

Will search twitter for the top K companies based on name or stock symbol, will then analyze tweet contents and determine sentiment value of the tweet.

Will then obtain stock closing vs opening prices

Dependencies:

  Requires Docker to be installed

To Build:

  run `docker build -t myapp .`

To Run (once finished):

  run `docker run myapp`

To Run a specific script:

  run `docker run myapp python app/twitterExtraction/retrieveTwitterData.py`
