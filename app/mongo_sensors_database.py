from pymongo import MongoClient

uri = "mongodb+srv://greenmind3.yasju.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=GreenMind3"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='./app/certs/sensors_db_cert.pem')

try:
    client.GreenMindSensorsAdmin.command("ping")
except Exception as e:
    print(e)

db = client.GreenMindSensorsData
sensors_db_collection = db["GreenMindSensorsData"]
