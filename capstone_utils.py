import pandas as pd

from surprise import Reader
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNWithZScore
from surprise import KNNBaseline
from surprise import SVD
from surprise import BaselineOnly
from surprise import SVDpp
from surprise import NMF
from surprise import SlopeOne
from surprise import CoClustering
from surprise.accuracy import rmse
from surprise import accuracy
from surprise.model_selection import train_test_split

def calculateSupriseDataSet(ds):
    ds = ds.filter(['user_pseudo_id', 'interest'])
    ds['count'] = 0
    ratingDS = ds.groupby(['user_pseudo_id', 'interest'])['count'].count().reset_index()

    ratingDS = ratingDS[ratingDS['count'] > 1]

    userSumListing = ratingDS.groupby(['user_pseudo_id'])['count'].max().reset_index()
    userSumListing.columns = ['user_pseudo_id', 'maxCount']

    rating = pd.concat([ratingDS.set_index('user_pseudo_id'), userSumListing.set_index('user_pseudo_id')], axis=1,
                       join='inner').reset_index()
    rating['rating'] = 5#round(50 * rating['count'] / rating['maxCount']) + 50

    final = rating.filter(['user_pseudo_id', 'interest', 'rating'])
    reader = Reader(rating_scale=(0, 100))
    return Dataset.load_from_df(final[['user_pseudo_id', 'interest', 'rating']], reader)



def calculateRMSEForVariousAlghoritms(data):
    benchmark = []
    # Iterate over all algorithms
    for algorithm in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(), KNNBasic(), KNNWithMeans(),
                      KNNWithZScore(), BaselineOnly(), CoClustering()]:
        # Perform cross validation
        results = cross_validate(algorithm, data, measures=['RMSE'], cv=3, verbose=False)

        # Get results & append algorithm name
        tmp = pd.DataFrame.from_dict(results).mean(axis=0)
        tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
        benchmark.append(tmp)

    surprise_results = pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse')
    print(surprise_results)