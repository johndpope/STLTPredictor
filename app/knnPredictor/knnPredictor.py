import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def KNN(sentiment, emotion):

    # name os csv file with train info (results.csv)
    #df = pd.read_csv('results.csv')

    # alternative for docker
    df = pd.read_csv('/app/results.csv')

    df.replace('?',-99999, inplace=True)

    # drop any unwanted fields
    df.drop(['Symbol'], 1, inplace=True)
    df.drop(['Start'], 1, inplace=True)
    df.drop(['Bullishness'], 1, inplace=True)

    X = np.array(df.drop(['Bullish'], 1))
    y = np.array(df['Bullish'])

    x_list = X.tolist()
    y_list = y.tolist()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

    # use k = 4 neighbors when predicting
    clf = neighbors.KNeighborsClassifier(3)

    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    #print"Testing Accuracy:", accuracy

    # this is what we want to predict on
    example_measures = np.array([sentiment, emotion])
    example_measures = example_measures.reshape(1, -1)

    prediction = clf.predict(example_measures)
    prediction_proba = clf.predict_proba(example_measures)

    """
    print "Bad Buy Probability:", prediction_proba.tolist()[0][0]
    print "Good Buy Probability:", prediction_proba.tolist()[0][1]
    print ""

    #print "Prediction: ", prediction_proba.tolist()[0][prediction[0]]

    if prediction.tolist()[0] == 0:
        print "Prediction: Bad Buy"
    else:
        print "Prediction: Good Buy"

    #print(prediction[0])
    """

    k_list = []     # build the good_buy class(k = black points)
    r_list = []     # build the bad_buy class (r= red points)

    point_i = 0
    for point in x_list:
        if y_list[point_i] == 1:        # check if weight is 1
            k_list.append(point)
        else:
            r_list.append(point)

        point_i += 1

    # add new point to graph
    new_features = [sentiment, emotion]

    # k and r will also be used for the color (black, red)
    dataset = { 'k': k_list, 'r': r_list }

    #print "dataset:", dataset

    black_patch = mpatches.Patch(color='black', label='Good Buy')
    red_patch = mpatches.Patch(color='red', label='Bad Buy')
    blue_patch = mpatches.Patch(color='blue', label='New Prediction')
    """
    plt.legend(handles=[black_patch, red_patch, blue_patch])

    [[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in dataset[i]] for i in dataset]
    plt.scatter(new_features[0], new_features[1], s=100,color="blue")

    plt.title('STLT Stock Predictor')
    plt.xlabel('Sentiment')
    plt.ylabel('Emotion')

    plt.savefig("/app/prediction_graph.png")
    """
    #plt.show()

    # returns 0 if bad buy, 1 if good buy
    return prediction[0].tolist(), prediction_proba.tolist()[0][prediction[0]]

if __name__ == "__main__":
    KNN(0.025, 0.0);


# some code obtained and adapted from https://pythonprogramming.net/programming-k-nearest-neighbors-machine-learning-tutorial
