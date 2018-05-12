import pandas as pd
import glob

#file = 'dataset.csv'
#file = 'Thammasat_Clean.csv'

file = 'dataset_1000.csv'
#file = 'Mahidol_Clean.csv'

data = pd.read_csv(file)
print data

