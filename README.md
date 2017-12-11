# STLTPredictor

Will search twitter for the top K companies based on name or stock symbol, will then analyze tweet contents and determine sentiment value of the tweet.

Will examine video and determine emotional score (normalized)

Will use kNN to predict whether you should make a purchase

Will use Bullishness vs. Bearishness to determine if stock should be purchased on known data


Dependencies:

  Requires Docker to be installed

To Build:

  run `docker build -t myapp .` (~7-8 minutes)

To Access docker machine in interactive mode (once finished building):

  run `docker run -it myapp /bin/bash`

Run the following once in the machine:

  run `python worker.py NKE_2012-08-16.mp4` or another video placed in the root folder (depends on length of video... ~30s to ~4-5 minutes)
  
-------------------------------------------------------------------

[Training] the CNN is different than predicting, to train follows the following steps (once in the docker environment):

    1) Once in docker (in interactive mode), go the the training directory 
        $ cd /app/app/emotion_tensorflow
        
    2) Then, run the following command:
        $ python train.py
        
Training will take a long time, anywhere from 30min-1hr.
