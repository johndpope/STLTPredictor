import sys
import os
sys.path.append("/app/app/emotion_tensorflow/")
import predict as emotionalRecognizer
sys.path.append("/app/app/twitterExtraction/")
import retrieveTwitterData as sentimentScorer
sys.path.append("/app/app/priceAnalysis/")
import retrievePriceData as priceAnalyzer
sys.path.append("/app/app/knnPredictor/")

def blockPrint():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
blockPrint()

import knnPredictor as Predictor
from ffmpy import FFmpeg

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

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
    enablePrint()
    if len(sys.argv) < 2:
        print "usage: python worker.py SYM_YYYY-MM-DD.mp4"
        sys.exit()
    if sys.argv[1] == "--help":
        print "pass in a .mp4 video file int the following format SYM_YYYY-MM-DD.mp4"
        print "worker will then parse the video file into its frames (2 fps by default)"
        print "retrieveTwitterData module is then called and returns a twitter sentiment score [-1, 1] based the SYM and date (looks at seven day period starting from YYYY-MM-DD)"
        print "emotionRecognizer module is then called and returns an emotional score [-1, 1] based on the frames found in the folder companies/SYM_YYYY-MM-DD"
        print "knnPredictor module is then called which takes the previously trained data in results.csv, sentiment, and emotional score as inputs, and returns a class prediction and probability of correctness"
        print "priceAnalyzer module is then called and takes as input the SYM and YYYY-MM-DD to determine the bullishness/bearishness of a stock over the 5-7 day period"
        print "to recieve additional information on any particular module, please navigate to the folder and examine the descriptions in the individual ReadMe"
    video_f = sys.argv[1]
    company_sym = video_f.partition("_")[0]
    date = video_f.partition("_")[2][:-4]
    directory = "/app/app/emotion_tensorflow/companies/" + video_f[:-4]
    try:
        os.makedirs(directory)
    except OSError as e:
        print "{0} already exists".format(directory)
        raise
    extractVideo(video_f, directory + "/" + company_sym + "_image_sequence%06d.png")

    print "determing sentiment score for {0} during the week {1}...".format(company_sym, date)
    sentiment_score = sentimentScorer.main(company_sym, date)
    print "sentiment score: {0}".format(sentiment_score)
    print "determining emotional score for frames found in {0}...".format(directory)
    emotional_score = emotionalRecognizer.predict("companies/" + video_f[:-4])
    print "emotional score: {0}".format(emotional_score)
    prediction, probability = Predictor.KNN(sentiment_score, emotional_score)
    print "you should {0} with probability {1}".format("BUY" if prediction == 1 else "NOT BUY", probability)

    # determine actual value
    #returns CompanyInfo object (defined in priceAnalyzer)
    print "determing actual results..."
    company = priceAnalyzer.analyzeTrends(company_sym, date)
    print "actual result is to {0}".format("BUY" if company.getBinaryResult() == 1 else "NOT BUY")
