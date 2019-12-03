import pandas as pd

# Importing the dataset
eventDataSet = pd.read_csv('data/FilteredEvents/capstone_event_2018_07.csv')
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_08.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_09.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_10.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_11.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2018_12.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_01.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_02.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_03.csv'))
eventDataSet = eventDataSet.append(pd.read_csv('data/FilteredEvents/capstone_event_2019_04.csv'))

#
#      listingType    count
# 0  GunlukKiralik    11237
# 1        Kiralik   672559
# 2        Kiralık   915960
# 3        Satilik   836634
# 4        Satılik  2017573
# 5        Satılık     3817

eventDataSet = eventDataSet.replace(to_replace=["Kiralık", "Satılik", "Satılık"], value = ["Kiralik", "Satilik", "Satilik"])

# eventDataSet = eventDataSet.filter(['listingType'])
# eventDataSet['count'] = 0
#
# ratingDS = eventDataSet.groupby(['listingType'])['count'].count().reset_index()
# print(ratingDS.head())

#      listingType    count
# 0  GunlukKiralik    11237
# 1        Kiralik  1588519
# 2        Satilik  2858024

eventDataSet = eventDataSet[(eventDataSet.districtName.notnull())]

salesEventDataSet = eventDataSet[(eventDataSet.listingTypeId == 1)]
rentEventDataSet = eventDataSet[(eventDataSet.listingTypeId == 2)]


