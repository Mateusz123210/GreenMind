from pymongo import MongoClient

uri = "mongodb+srv://greenmind2.p54ki.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=GreenMind2"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='./app/certs/predictions_db_cert.pem')

try:
    client.GreenMindPredictionsAdmin.command("ping")
except Exception as e:
    print(e)

db = client.GreenMindPredictions
predictions_db_collection = db["GreenMindPredictions"]
