from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["studio_data"]
collection = db["report"]

data = [
    {"name": "Báo cáo cuộc gọi tháng 5", "slug": "72ca60bb-a2f2-4ad4-8405-4fe19695af46", "type": "weekly", "date": "15/02/2024"},
]

collection.insert_many(data)

print("heh")
