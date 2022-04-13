import pandas as pd
import numpy as np

##### CLUSTERING NTT

df = pd.read_csv("customer_dataset.csv", sep=";")

df = df[df.automotive != "#N/D"]

productcategory_names = ['agriculture suppliers', 'automotive',
       'bakeware', 'beauty & personal care', 'bedroom decor', 'book',
       'business office', 'camera & photo', 'cd vinyl', 'ceiling fans',
       'cell phones', 'cleaning supplies', 'coffee machines', 'comics',
       'computer accessories', 'computers tablets', 'diet sports nutrition',
       'dvd', 'event & party supplies', 'fabric', 'fashion & shoes',
       'film & photography', 'fire safety', 'food', 'fragrance', 'furniture',
       'handbags & accessories', 'hardware', 'headphones', 'health household',
       'home accessories', 'home appliances', 'home audio',
       'home emergency kits', 'home lighting', 'home security systems',
       'jewelry', 'kids', 'kids fashion', 'kitchen & dining', 'lawn garden',
       'light bulbs', 'luggage', 'mattresses & pillows', 'medical supplies',
       "men's fashion", 'model hobby building', 'monitors',
       'music instruments', 'office products', 'oral care', 'painting',
       'pet food', 'pet supplies', 'safety apparel', 'seasonal decor', 'sofa',
       'sport outdoors', 'television & video', 'tools home improvement',
       'toys games', 'underwear', 'videogame', 'videogame console', 'wall art',
       'watches', 'wellness & relaxation', "woman's fashion"]

df[productcategory_names] = df[productcategory_names].apply(pd.to_numeric, errors='coerce')



column_names_home = ['bakeware', 'bedroom decor', 'cleaning supplies',
                     'home accessories', 'home appliances', 'home audio',
                     'home emergency kits', 'home lighting', 'home security systems',
                     'health household', 'kitchen & dining', 'mattresses & pillows',
                     'seasonal decor', 'tools home improvement', 'wall art',
                     'event & party supplies', 'luggage', 'medical supplies', 'pet food',
                     'pet supplies', 'food', 'kids', 'toys games']
df['Home']= df[column_names_home].sum(axis=1)


column_names_forniture = ['ceiling fans', 'coffee machines', 'business office','furniture',
                          'light bulbs', 'office products', 'fire safety', 'automotive', 'sofa']
df['Forniture']= df[column_names_forniture].sum(axis=1)

column_names_tech = ['camera & photo', 'cd vinyl', 'cell phones', 'computer accessories', 'computers tablets','dvd',
                     'film & photography', 'hardware', 'headphones', 'monitors', 'television & video',
                     'videogame', 'videogame console']
df['Technology']= df[column_names_tech].sum(axis=1)

column_names_fashion =['beauty & personal care', 'fashion & shoes', 'fabric',
                       'handbags & accessories', 'fragrance','jewelry', "men's fashion", 'underwear',
                       'watches', 'wellness & relaxation',"woman's fashion", 'kids fashion',
                       'diet sports nutrition', 'oral care', 'safety apparel']
df['Fashion/Personal care']= df[column_names_fashion].sum(axis=1)


column_names_hobbies = ['agriculture suppliers', 'book', 'comics','lawn garden',
                        'model hobby building', 'painting','sport outdoors', 'music instruments']
df['Hobbies']= df[column_names_hobbies].sum(axis=1)

del column_names_home
del column_names_tech
del column_names_fashion
del column_names_forniture
del column_names_hobbies
del productcategory_names

df_cluster = df[['customer_unique_id', "order_count (only positive orders)", "product count", "review_rate (n. recensioni / n. prodotti acquistati)",
         "score_medio_reviews", "costoprodotti_medio", "spedizioni_medie",
         "most_used_paym_meth", "n_medio_pagamenti", "n_medio_rate", "most_frequent_time_bin",
                 "most_frequent_weekday_bin", "most_frequent_month_bin",
                 'Home', 'Forniture', 'Technology', 'Fashion/Personal care', 'Hobbies' ]]

df_cluster = df_cluster.replace('#N/D', np.NaN)

'''
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore')
# passing bridge-types-cat column (label encoded values of bridge_types)
enc_df = pd.DataFrame(enc.fit_transform(df_cluster[['most_used_paym_meth']]).toarray())
# merge with main df bridge_df on key values
df_cluster = df_cluster.join(enc_df)
'''

dummy_df = pd.get_dummies(df_cluster["most_used_paym_meth"])
df_cluster = df_cluster.drop(["most_used_paym_meth"], axis=1)
df_cluster = df_cluster.join(dummy_df)

for column in df_cluster.columns[1:]:
    df_cluster[column] = pd.to_numeric(df_cluster[column])
    df_cluster[column].fillna((df_cluster[column].median()), inplace=True)



from sklearn.preprocessing import StandardScaler
x = df_cluster.iloc[:, df_cluster.columns != "customer_unique_id"].values
x = StandardScaler().fit_transform(x) # normalizing the features


from sklearn.decomposition import PCA
pca_breast = PCA(n_components=8)
principalComponents_breast = pca_breast.fit_transform(x)
#principal_breast_Df = pd.DataFrame(data = principalComponents_breast
#             , columns = ['principal component 1', 'principal component 2'])


print('Explained variation per principal component: {}'.format(pca_breast.explained_variance_ratio_))

# >> Explained variation per principal component: [0.36198848 0.1920749 ]

print('Cumulative variance explained by 2 principal components: {:.2%}'.format(np.sum(pca_breast.explained_variance_ratio_)))



