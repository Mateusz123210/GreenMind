import os
os.system("docker build . -t backend11")
os.system("docker tag backend11 kubregistry2.azurecr.io/backend11:latest")
os.system("docker push kubregistry2.azurecr.io/backend11:latest")