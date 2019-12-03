# importing the requests library
import requests
import csv
import time

def writeToCsv(writer, l, no):
    writer.writerow({
        "no": no,
        "id": l["id"],
        "listingType": "satilik",
        "type": l["property"]["type"]["name"],
        "price": l["price"]["amount"],
        "currency": l["price"]["currency"],
        "basePrice": l["basePrice"]["amount"],
        "baseCurrency": l["basePrice"]["currency"],
        "roomCount": l["property"]["roomCount"],
        "roomSlug": l["property"]["roomSlug"],
        "size": l["property"]["size"],
        "cityId": l["property"]["location"]["city"]["id"],
        "cityName": l["property"]["location"]["city"]["name"],
        "countyId": l["property"]["location"]["county"]["id"],
        "countyName": l["property"]["location"]["county"]["name"],
        "districtId": l["property"]["location"]["id"],
        "districtName": l["property"]["location"]["name"]
    })
    no += 1


def request(writer, locId, pageNo, no):
    # api-endpoint
    URL = "https://mapi.zingat.com/listing?page={}&page_size=100&listingTypeId=1&propertyTypeId=79&locationId[]={}".format(pageNo, locId)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 8b970afbe15ad12f62cfef0a7947fd23f809cec4"
    }

    r = requests.get(url=URL, headers=headers)
    data = r.json()

    if("facets" not in data):
        print(f'{locId} lokasyonu tamamlandı')
        return no

    if("county" in data["facets"]):
        print(f'{locId} bir şehirdir')
        return no

    if("district" in data["facets"]):
        print(f'{locId} bir ilçedir')
        return no

    if("listing" not in data["_embedded"]):
        return no

    if(len(data["_embedded"]["listing"]) == 0):
        return no

    print(f'{locId} lokasyonu için {pageNo} sayfası başladı')
    for l in data["_embedded"]["listing"]:
        writeToCsv(writer, l, no)
        no += 1
    print(f'{locId} lokasyonu için {pageNo} sayfası bitti')

    time.sleep(0.2)
    return request(writer, locId, pageNo + 1, no)




# sending get request and saving the response as response object

#print("%s", r.content)


#print(len(data["_embedded"]["listing"]))


#l = data["_embedded"]["listing"][0]

#with open('sales.csv', mode='a') as csv_file:
#    fieldnames = ["id", "listingType", "type", "price", "currency", "basePrice", "baseCurrency", "roomCount", "roomSlug", "size", "cityId", "cityName", "countyId", "countyName", "districtId", "districtName"]
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    writer.writeheader()

print("işleme başladım")
with open('sales.csv', mode='a') as csv_file:
    fieldnames = ["no", "id", "listingType", "type", "price", "currency", "basePrice", "baseCurrency", "roomCount", "roomSlug",
                  "size", "cityId", "cityName", "countyId", "countyName", "districtId", "districtName"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #for l in data["_embedded"]["listing"]:
    #    writeToCsv(writer, l)
    no = 1
    for i in range(1, 1001):
        print(f'\t{i} lokasyonu')
        no = request(writer, i, 1, no)


print("işlemi bitirdims")




