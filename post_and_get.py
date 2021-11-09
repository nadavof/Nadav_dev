import requests
import numpy as np


BASE = "http://127.0.0.1:5000/"
FEATURES_LENGHT = 256
 
NAMES_EXAMPLE = ["Orly", "Yoram", "Matan", "Nadav", "Stav", "Chen", "Dauber", "Amrani", "Markman", "Ron"]


data =[]



#Generating random features
for i, name in enumerate(NAMES_EXAMPLE):
    data.append({"name": name, "features" : np.random.rand(FEATURES_LENGHT)})
    print(f"Adding to DB person: {data[i]}")
    #clean DB for debug
    respose = requests.delete(BASE + f"person/{name}")

#for testing
#data = [{'name': 'Nadav', 'features':  np.array([0.98,0.92,0.91])}, {'name': 'Markman', 'features':  np.array([0.39,0.61,0.81])}, {'name': 'Ron', 'features':  np.array([0.4,0.6,0.8])}]

for i in range(len(data)):
   # print('This data was sent:', str(i), data[i])
    respose = requests.post(BASE + "person/" + str(i), data[i])
    #respose = requests.post(BASE + "person", {"name" : name, "features" : persons[name]})
    print(respose.json())

for i in range(len(data)):
    print(f'Searching for the closest person to: {data[i]["name"]}...')
    respose = requests.get(BASE + f"person/Yoram", {'features': data[i]["features"]})
    print(respose.json())


