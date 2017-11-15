# STLTPredictor

Will search twitter for the top K companies based on name or stock symbol, will then analyze tweet contents and determine sentiment value of the tweet.


Dependencies:
`pip install -r ./static/requirements.txt`

Depending on on your system, you might need to change the limit on open file descriptors allowed.

You can check with `ulimit -a`, it seems we might need at least ~600, and you can change this with `ulimit -n value`
