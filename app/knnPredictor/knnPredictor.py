import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd

def KNN(sentiment, emotion):
    
    # name os csv file with train info (results.csv)
    df = pd.read_csv('results.csv')
    df.replace('?',-99999, inplace=True)

    # drop any unwanted fields
    df.drop(['Symbol'], 1, inplace=True)
    df.drop(['Start'], 1, inplace=True)

    X = np.array(df.drop(['Bullishness'], 1))
    y = np.array(df['Bullishness'])

    print "*****X:", X.tolist()
    print "&&&&&Y:", y.tolist()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

    clf = neighbors.KNeighborsClassifier()

    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    print(accuracy)

    # this is what we want to predict
    #example_measures = np.array([4,2,1,1,1,2,3,2,1])

    example_measures = np.array([sentiment, emotion])
    example_measures = example_measures.reshape(1, -1)

prediction = clf.predict(example_measures)
print(prediction)

if __name__ == "__main__":
    KNN(0.4, 0.2);
