import requests
import numpy as np


BASE = "http://127.0.0.1:5000/"
FEATURES_LENGHT = 256
 
NAMES_EXAMPLE = ["Orly", "Yoram", "Matan", "Nadav", "Stav", "Chen", "Dauber", "Amrani", "Markman", "Ron"]


data =[]

f = np.array([0.98,0.92,0.91])



#Generating random features
for i, name in enumerate(NAMES_EXAMPLE):
    data.append({"name": name, "features" : np.random.rand(FEATURES_LENGHT)})
    #data.append({"name": name, "features": np_arrays[i]})
    #print(f"Adding to DB person: {data[i]}")

    respose = requests.delete(BASE + f"person/{name}")

for i in range(len(data)):
    #generating persons & features pair
    respose = requests.post(BASE + "person/" + str(i), data[i])
    print(respose.json())

