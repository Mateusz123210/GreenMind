import os
os.system("docker build . -t backend11")
os.system("docker tag backend11 kubregistry1.azurecr.io/backend11:latest")
os.system("docker push kubregistry1.azurecr.io/backend11:latest")