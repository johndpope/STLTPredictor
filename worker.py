import sys
sys.path.append("/app/app/emotion_tensorflow/")
import predict as emotionalRecognizer
sys.path.append("/app/app/twitterExtraction/")
import retrieveTwitterData as sentimentScorer
from ffmpy import FFmpeg
import os
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def extractVideo(video_f, directory):
    ff = FFmpeg(
        inputs={video_f: None},
        outputs={directory: ['-r', '2']}
    )
    print "parsing video..."
    blockPrint()
    ff.run(stdout=sys.stdout, stderr=sys.stdout)
    enablePrint()

if __name__ =="__main__":
    if len(sys.argv) < 2:
        print "usage: python worker.py SYS_YYYY-MM-DD.mp4"
        sys.exit()
    video_f = sys.argv[1]
    company_sym = video_f.partition("_")[0]
    date = video_f.partition("_")[2][:-4]
    directory = "/app/app/emotion_tensorflow/companies/" + video_f[:-4]
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    extractVideo(video_f, directory + "/" + company_sym + "_image_sequence%06d.png")

    print "determing sentiment score..."
    sentiment_score = sentimentScorer.main(company_sym, date)
    print "sentiment score: {0}".format(sentiment_score)
    print "determining emotional score..."
    emotional_score = emotionalRecognizer.predict('companies/MCD', 'extract')
    print "emotional score: {0}".format(emotional_score)
