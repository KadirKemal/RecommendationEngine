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

# Importing the dataset
dataset_2018_07 = pd.read_csv('data/FilteredEvents/capstone_event_2018_07.csv')
dataset_2018_08 = pd.read_csv('data/FilteredEvents/capstone_event_2018_08.csv')

ds = dataset_2018_07.append(dataset_2018_08)
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_09.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_10.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_11.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_12.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_01.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_02.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_03.csv'))
ds = ds.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_04.csv'))

ds = ds[ds.listingTypeId == 1 & (ds.listingType.notnull()) & (ds.districtName.notnull())]
ds["interest"] = ds.listingType + "_" + ds.cityName + "_" + ds.countyName + "_" + ds.districtName

ds = ds.filter(['user_pseudo_id', 'interest'])
ds['count'] = 0
ratingDS = ds.groupby(['user_pseudo_id', 'interest'])['count'].count().reset_index()

userSumListing = ratingDS.groupby(['user_pseudo_id'])['count'].max().reset_index()
userSumListing.columns = ['user_pseudo_id', 'maxCount']

print(ratingDS.head())
print(userSumListing.head())

rating = pd.concat([ratingDS.set_index('user_pseudo_id'), userSumListing.set_index('user_pseudo_id')], axis=1, join='inner').reset_index()
print(rating.head())

rating['rating'] = round(4 * rating['count'] / rating['maxCount']) + 1
print(rating.head())


#top10 = populer.nlargest(10, 'count')
#top10 = populer.nsmallest(10, 'count')
#print(top10)

#populer = populer.groupby(['count']).count().reset_index()

#print(len(populer))
#print(populer)


final = rating.filter(['user_pseudo_id', 'interest', 'rating'])

print(final.head())





#abc(final)

reader = Reader(rating_scale=(0, 5))
data = Dataset.load_from_df(final[['user_pseudo_id', 'interest', 'rating']], reader)

print('Using KNNBasic')
bsl_options = {'method': 'als',
               'n_epochs': 5,
               'reg_u': 12,
               'reg_i': 5
               }
#algo = BaselineOnly(bsl_options=bsl_options)
#cross_validate(algo, data, measures=['RMSE'], cv=3, verbose=False)

trainset, testset = train_test_split(data, test_size=0.25)
algo = KNNBasic(bsl_options=bsl_options)
algo.fit(trainset)
predictions = algo.test(testset)
accuracy.rmse(predictions)

result = pd.DataFrame(predictions, columns=['visitor_id', 'item_id', 'base_event', 'predict_event', 'details'])
result.drop(columns={'details'}, inplace=True)
result['erro'] = abs(result['base_event'] - result['predict_event'])
print(result.head())


tuzlaId = algo.trainset.to_inner_iid('Satılik_İstanbul_Tuzla_İçmeler')
print("Satılik_İstanbul_Tuzla_İçmeler : " + tuzlaId)
tuzla_neighbors = algo.get_neighbors(tuzlaId, k=5)
tuzla_neighbors = (algo.trainset.to_raw_iid(tuzlaId) for tuzlaId in tuzla_neighbors)

for n in tuzla_neighbors:
    print(n)