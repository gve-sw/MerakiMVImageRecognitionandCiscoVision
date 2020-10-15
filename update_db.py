from env_var import Database, Cluster, Collection
from pymongo import MongoClient
from datetime import datetime

#Connection with the MongoDB
def get_collection():
    cluster = MongoClient(Database)
    db = cluster[Cluster]
    collection = db[Collection]
    return collection

#Inserts the details into the Database for recording purposes
def database_update(sex, age, tag):
    date = datetime.now()
    today = date.strftime('%H:%M %m-%d-%Y')
    collection = get_collection()
    collection.insert_one({"sex": sex, "age": age, "tag": tag,  'update_date': today})
