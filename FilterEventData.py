import pandas as pd
from numpy import nan as Nan
import datetime
import threading
import calendar


def work(filename, startDate, endDate):
    print(datetime.datetime.now().strftime("%X") + " - " + filename + " işe başladı!")

    eventDate = startDate

    correctColumns = {'CountyId': 'countyId',
                      'CityId': 'cityId',
                      'DistrictId': 'districtId',
                      'cistrictId': 'districtId',
                      'county': 'countyName',
                      'County': 'countyName',
                      'district': 'districtName',
                      'District': 'districtName',
                      'city': 'cityName',
                      'City': 'cityName',
                      'ListingTypeId': 'listingTypeId',
                      'ListingType': 'listingType',
                      'ListingId': 'listingId',
                      'ProjectId': 'projectId',
                      'PropertyType': 'propertyType',
                      'PropertyTypeId': 'propertyTypeId',
                      'SubPropertyType': 'subPropertyType'}

    columList = ['event_date', 'event_timestamp', 'user_pseudo_id', 'event_name', 'listingId']
    columList = columList + ['listingType', 'listingTypeId', 'subPropertyTypeId']
    columList = columList + ['propertyType', 'propertyTypeId', 'subPropertyType']
    columList = columList + ['cityId', 'cityName']
    columList = columList + ['countyId', 'countyName']
    columList = columList + ['districtId', 'districtName']

    header = True
    while (eventDate < endDate):
        print(datetime.datetime.now().strftime("%X") + " - " + filename + " şu tarihte :" + eventDate.strftime("%Y%m%d"))
        df = pd.DataFrame(columns=columList)

        s = "data/events/" + eventDate.strftime("%Y%m%d") + ".json"
        #print(s)
        a = pd.read_json(s, orient='records')
        # print(len(a))

        #print(datetime.datetime.now())
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

        print(datetime.datetime.now().strftime("%X") + " - " + filename + " şu tarihi bitirdi :" + eventDate.strftime("%Y%m%d"))
        #print(len(df))
        with open("data/FilteredEvents/capstone_event_" + filename + ".json", 'a') as f:
            df.to_csv(f, header=header)
        header = False

        eventDate = eventDate + datetime.timedelta(days=1)

    print(datetime.datetime.now().strftime("%X") + " - " + filename + " işi bitirdi!")

eventDate = datetime.date(2018, 11, 1)
while(eventDate < datetime.date(2019, 5, 1)):

    days_in_month = calendar.monthrange(eventDate.year, eventDate.month)[1]
    lastDate = eventDate + datetime.timedelta(days=days_in_month)
    x = threading.Thread(target=work, args=(eventDate.strftime("%Y%m"), eventDate, lastDate))
    x.start()

    eventDate = lastDate