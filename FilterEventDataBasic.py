import pandas as pd
from numpy import nan as Nan
import datetime

correctColumns = {'CountyId': 'countyId',
                  'CityId' : 'cityId',
                  'DistrictId' : 'districtId',
                  'cistrictId' : 'districtId',
                  'county': 'countyName',
                  'County': 'countyName',
                  'district': 'districtName',
                  'District': 'districtName',
                  'city': 'cityName',
                  'City': 'cityName',
                  'ListingTypeId' : 'listingTypeId',
                  'ListingType': 'listingType',
                  'ListingId' : 'listingId',
                  'ProjectId' : 'projectId',
                  'PropertyType' : 'propertyType',
                  'PropertyTypeId' : 'propertyTypeId',
                  'SubPropertyType' : 'subPropertyType'}


columList = ['event_date', 'event_timestamp', 'user_pseudo_id', 'event_name', 'listingId']
columList = columList + ['listingType', 'listingTypeId', 'subPropertyTypeId']
columList = columList + ['propertyType', 'propertyTypeId', 'subPropertyType']
columList = columList + ['cityId', 'cityName']
columList = columList + ['countyId', 'countyName']
columList = columList + ['districtId', 'districtName']

print(columList)

header = False

eventDate = datetime.date(2019, 4, 12)
while(eventDate < datetime.date(2019, 5, 1)):
    print(datetime.datetime.now().strftime("%X") + " şu tarihteyim :" + eventDate.strftime("%Y%m%d"))

    df = pd.DataFrame(columns=columList)

    s = "data/events/" + eventDate.strftime("%Y%m%d")+".json"
    a = pd.read_json(s, orient='records')
    # print(len(a))

    print(datetime.datetime.now())
    for i in range(0, len(a)):
        item = a.iloc[i]

        if item["event_name"] != "ListingView" or item["event_params"] is None:
            continue

        index = len(df)
        df.loc[index] = [Nan] * len(df.columns)

        df.loc[index]["event_date"] = item["event_date"]
        df.loc[index]["event_timestamp"] = item["event_timestamp"]
        df.loc[index]["user_pseudo_id"] = item["user_pseudo_id"]
        df.loc[index]["event_name"] = item["event_name"]

        params = item["event_params"]
        for item in params:
            key = item['key']
            value = item['value']
            pureValue = value['string_value'] or value['int_value'] or value['float_value'] or value['double_value']

            if key in correctColumns:
                key = correctColumns[key]

            if key in columList:
                df.loc[index][key] = pureValue

    print(datetime.datetime.now().strftime("%X") + " şu tarihi bitirdim :" + eventDate.strftime("%Y%m%d"))

    with open("data/FilteredEvents/capstone_event_2019_04.json", 'a') as f:
        df.to_csv(f, header=header)
    header = False

    eventDate = eventDate + datetime.timedelta(days=1)
