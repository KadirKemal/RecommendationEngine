import csv

fieldnames = ["no",
              "id", "listingType", "type", "price", "currency", "basePrice", "baseCurrency", "roomCount", "roomSlug", "size", "cityId", "cityName", "countyId", "countyName", "districtId", "districtName"]

with open('sales.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        if line_count == 3:
            break

        print(f'id: {row["id"]}, listingType: {row["listingType"]}, type: {row["type"]}')
        for f in fieldnames:
            print(f'{f}: {row[f]}')
        print("-------------")
        line_count += 1
    print(f'Processed {line_count} lines.')




#id,listingType,type,price,currency,basePrice,baseCurrency,roomCount,roomSlug,size,cityId,cityName,countyId,countyName,districtId,districtName
