import pandas as pd


a = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 3, 4]})
b = pd.DataFrame({'a': [1, 2, 3], 'b': [22, 33, 44]})
a.loc[7] = [7, 7]
a.loc[4] = [4, 4]
print(pd.concat([a, b]))

df_out = pd.DataFrame(columns=('a', 'b'))
print(df_out)
df_out.loc[2] = [8, 8]
print(df_out)

date = "0816"
filePath1 = '../data/' + date + '/research.csv'
filePath2 = '../data/' + date + '/gasUsed.csv'
outputPath = '../data/' + date + '/output.csv'
print(outputPath)