import pandas as pd
import matplotlib.pyplot as plt


def createPopulerCitiesChart(ds):
    populer = ds
    populer['count'] = 0
    populer = populer.groupby(['cityName'])['count'].count().reset_index()
    top10 = populer.nlargest(10, 'count')

    print(top10)

    top10.plot.bar(figsize=[16, 6], x='cityName', fontsize=12, title='Top 10 City').title.set_size(16)
    plt.show()


def createPopulerCountiesChart(ds):
    populer = ds
    populer['count'] = 0
    populer = populer.groupby(['cityName', 'countyName'])['count'].count().reset_index()
    top10 = populer.nlargest(10, 'count')

    print(top10)

    top10.plot.bar(figsize=[16, 6], x='countyName', fontsize=12, title='Top 10 County').title.set_size(16)
    plt.show()


def createPopulerDistirctsChart(ds):
    populer = ds
    populer['count'] = 0
    populer = populer.groupby(['cityName', 'countyName', 'districtName'])['count'].count().reset_index()
    top10 = populer.nlargest(10, 'count')

    print(top10)

    top10.plot.bar(figsize=[16, 6], x='districtName', fontsize=12, title='Top 10 District').title.set_size(16)
    plt.show()


# Importing the dataset
dataset_2018_07 = pd.read_csv('data/FilteredEvents/capstone_event_2018_07.csv')
dataset_2018_08 = pd.read_csv('data/FilteredEvents/capstone_event_2018_08.csv')

print(len(dataset_2018_07))
print(len(dataset_2018_08))

ds = dataset_2018_07.append(dataset_2018_08)

print(len(ds))


createPopulerDistirctsChart(ds)








