import pandas as pd

# Importing the dataset
listingDataSet = pd.read_csv('data/listing/listing0.csv')

for i in range(1, 668):
    filePath = 'data/listing/listing'+str(i)+'.csv'
    listingDataSet = listingDataSet.append(pd.read_csv(filePath))