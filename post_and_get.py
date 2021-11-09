import requests
import numpy as np
import pandas as pd

BASE = "http://127.0.0.1:5000/"
FEATURES_LENGHT = 3 #256
 
NAMES_EXAMPLE = ["Orly", "Yoram", "Matan", "Nadav", "Stav", "Chen", "Dauber", "Amrani", "Markman", "Ron"]
#NAMES_EXAMPLE = ["Orly", "Yoram", "Matan", "Nadav", "Stav"]

data =[]
# a = np.array([1,2,3])
# b = np.array([1,3,3])
# c = np.array([3,4,17])
# d = np.array([1,16,13])
# e = np.array([2,3,4])

f = np.array([0.98,0.92,0.91])

#np_arrays = [a, b, c, d, e]

#Generating random features
for i, name in enumerate(NAMES_EXAMPLE):
    data.append({"name": name, "features" : np.random.rand(FEATURES_LENGHT)})
    #data.append({"name": name, "features": np_arrays[i]})
    print(f"Adding to DB person: {data[i]}")
    respose = requests.delete(BASE + f"person/{name}")

#for testing
data = [{'name': 'Nadav', 'features':  np.array([0.98,0.92,0.91])}, {'name': 'Markman', 'features':  np.array([0.39,0.61,0.81])}, {'name': 'Ron', 'features':  np.array([0.4,0.6,0.8])}]

for i in range(len(data)):
    print('This data was sent:', str(i), data[i])
    respose = requests.post(BASE + "person/" + str(i), data[i])
    #respose = requests.post(BASE + "person", {"name" : name, "features" : persons[name]})
    print(respose.json())

for i in range(len(data)):
    print(f'Searching for the closest person to: {data[i]["name"]}...')
    respose = requests.get(BASE + f"person/Yoram", {'features': data[i]["features"]})
    print(respose.json())

#respose = requests.delete(BASE + "person/Orly")
#input()

#respose = requests.get(BASE + "person/Yoram")





# def dot_product(data_test, search):
#     res = []
#     for key, val in data_test.items():
#         res.append({"name" :  key, "distance": np.dot(search/search.sum(), val/val.sum())})
#     newlist = sorted(res, key=lambda d: d['distance'], reverse=True)
#     return newlist
# a = np.array([1,2,3])
# norm_a = np.linalg.norm(a)
# normal_array_a = a/norm_a
#
# b = np.array([1,2,3])
# norm_b = np.linalg.norm(b)
# normal_array_b = b/norm_b
# print(np.dot(normal_array_b, normal_array_a))
#
# b = np.array([1,5,10])
# c = np.array([1,15,16])
# d = np.array([1,6,13])
# e = np.array([1,5,12])
#
# #s= pd.Series([1,5,12])
#
# np_arrays = [a, b, c, d]
# data_test = {}
# for i, name in enumerate(['A', 'B', 'C', 'D']):
#     data_test[name] = np_arrays[i]
#
#
# #df = pd.DataFrame.from_dict(data_test)
# #df = pd.DataFrame.from_dict(data_test, dtype='ndarray')
#
# # for index, row in df.iterrows():
# #     df['dot_product'][index] = np.dot(e, row['features'][index])
#
# res = dot_product(data_test, e)
#
# ############
# def get_closest(db, input_person):
#     res = []
#     for key, val in db.items():
#         res.append({"name" :  key, "distance": np.dot(input_person/input_person.sum(), val/val.sum())})
#     top_3 = sorted(res, key=lambda d: d['distance'], reverse=True)[:3]
#     return [d['name'] for d in top_3]
#
#
# ############
#
# n=1

