import json

filename = "appliance_db.json"

data = {"Bosch Vacuum": "faiss_index/Bosch Vacuum"}

with open(filename, "a") as f:
    file = json.dump(data, f)
    print(file)


lst = [appliance for appliance in data]
print(lst)
