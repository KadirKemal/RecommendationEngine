import csv

with open('sales.csv', mode='w') as csv_file:
    fieldnames = ["no", "id", "listingType", "type", "price", "currency", "basePrice", "baseCurrency", "roomCount", "roomSlug", "size", "cityId", "cityName", "countyId", "countyName", "districtId", "districtName"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()