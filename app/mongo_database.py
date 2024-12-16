from pymongo import MongoClient

uri = "mongodb+srv://greenmind1.lgvzz.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=GreenMind1"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='./app/certs/X509-cert-7343365104670543246.pem')

try:
    client.GreenMindWeatherAdmin.command("ping")
except Exception as e:
    print(e)

db = client.GreenMindWeatherData
collection_green_mind = db["GreenMindWeatherData"]