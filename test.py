from capstone_loadEventData import salesEventDataSet
from capstone_utils import *


ds = salesEventDataSet[(salesEventDataSet.cityId == 1) & (salesEventDataSet.subPropertyType.notnull()) & (salesEventDataSet.subPropertyType == 'Daire')]
ds["interest"] = ds.cityName + "_" + ds.countyName + "_" + ds.districtName #+ "_" + ds.subPropertyType
ds = ds.filter(['user_pseudo_id', 'interest'])
ds['count'] = 0
ratingDS = ds.groupby(['user_pseudo_id', 'interest'])['count'].count().reset_index()


userSumListing = ratingDS.groupby(['user_pseudo_id'])['count'].max().reset_index()
userSumListing.columns = ['user_pseudo_id', 'maxCount']

rating = pd.concat([ratingDS.set_index('user_pseudo_id'), userSumListing.set_index('user_pseudo_id')], axis=1,
                   join='inner').reset_index()
rating['rating'] = round(3 * rating['count'] / rating['maxCount']) + 2

final = rating.filter(['user_pseudo_id', 'interest', 'rating'])
reader = Reader()
data = Dataset.load_from_df(final[['user_pseudo_id', 'interest', 'rating']], reader)

#data = calculateSupriseDataSet(salesEventDataSet)

# calculateRMSEForVariousAlghoritms(data)

def generateModelWithBestAlghoritm():
    print('Using KNNBasic')
    trainset, testset = train_test_split(data, test_size=0.80)
    algo = KNNBasic()
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions)

    result = pd.DataFrame(predictions, columns=['visitor_id', 'item_id', 'base_event', 'predict_event', 'details'])
    result.drop(columns={'details'}, inplace=True)
    result['erro'] = abs(result['base_event'] - result['predict_event'])
    print(result.head())


    id = algo.trainset.to_inner_iid('İstanbul_Kağıthane_Nurtepe')

    print("****" + algo.trainset.to_raw_iid(id) + "****")
    neighbors = algo.get_neighbors(id, k=5)
    neighbors = (algo.trainset.to_raw_iid(id) for id in neighbors)

    for n in neighbors:
        print(n)

generateModelWithBestAlghoritm()


#
# SVD              15.661373    3.666409   0.284029
# BaselineOnly     16.084185    0.274930   0.236176
# KNNBaseline      16.279271   23.598579   9.661409
# KNNWithMeans     17.393004   25.361248   8.854265
# SlopeOne         17.498504    0.361450   0.551343
# KNNWithZScore    17.642407  102.068461   9.400655
# CoClustering     17.831922    3.861177   0.266781
# SVDpp            18.228711   15.107624   0.779263
# KNNBasic         18.556711   24.970789   8.521991
# NormalPredictor  25.650519    0.126029   0.355960
# NMF              60.644808    5.692924   0.245301
