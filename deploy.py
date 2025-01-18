import os
os.system("docker build . -t backend4")
os.system("docker tag backend4 kubregistry2.azurecr.io/backend4:latest")
os.system("docker push kubregistry2.azurecr.io/backend4:latest")