import pandas as pd
import matplotlib.pyplot as plt
import math


def pilotPriceHistogram(ds):
    #ds.hist(column="price")
    #plt.show()

    price_ds = ds
    price_ds['priceGroup'] = math.floor(price_ds['price'] / 500)
    price_ds = price_ds.groupby('priceGroup')['priceGroup'].count().reset_index(name='count')
    price_ds.plot.bar(figsize=[16, 6], x='priceGroup', fontsize=12, title='Price Groups').title.set_size(16)
    plt.show()


def pilotRoomCountHistogram(ds):
    #ds.hist(column="roomCount")
    #plt.show()

    roomSlug_ds = ds.groupby('roomSlug')['roomSlug'].count().reset_index(name = 'count')
    roomSlug_ds.plot.bar(figsize=[16, 6], x='roomSlug', fontsize=12, title='Room Slugs of Listings').title.set_size(16)
    plt.show()

#paldır
#borik asit

def pilotTypeHistogram(ds):
    type_ds = ds.groupby('type')['type'].count().reset_index(name = 'count')
    type_ds.plot.bar(figsize=[16, 6], x='type', fontsize=12, title='Type of Listings').title.set_size(16)
    plt.show()

# Importing the dataset
ds = pd.read_csv('data/listing/listing0.csv')
for i in range(1,5):
    temp = pd.read_csv("data/listing/listing"+str(i)+".csv")
    ds = ds.append(temp)

print(len(ds))
print(ds.info())

#no,id,listingType,type,parentType,price,currency,basePrice,baseCurrency,roomCount,livingRoomCount,roomSlug,size,cityId,cityName,countyId,countyName,districtId,districtName
#398,1684142,Rent,Daire,Konut,3600,TRY,3600,TRY,2,1,2 + 1,110,1,İstanbul,156,Beşiktaş,162,Gayrettepe
besiktas_rent = ds[(ds.countyId == 156) & (ds.listingType == 'Rent') & (ds.price.notnull())]
besiktas_sale = ds[(ds.countyId == 156) & (ds.listingType == 'Sale') & (ds.price.notnull())]

gayrettepe_rent = ds[(ds.countyId == 162) & (ds.listingType == 'Rent') & (ds.price.notnull())]
gayrettepe_sale = ds[(ds.countyId == 162) & (ds.listingType == 'Sale') & (ds.price.notnull())]


pilotPriceHistogram(besiktas_rent)
pilotRoomCountHistogram(besiktas_rent)
pilotTypeHistogram(besiktas_rent)