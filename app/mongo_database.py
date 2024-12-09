from pymongo import MongoClient

uri = "mongodb+srv://greenmind3.yasju.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=GreenMind3"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='./app/certs/X509-cert-2028425396859799908.pem')

try:
    client.GreenMindSensorsAdmin.command("ping")
except Exception as e:
    print(e)

db = client.GreenMindSensorsData
collection_green_mind = db["GreenMindSensorsData"]