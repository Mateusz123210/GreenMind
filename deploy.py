import os
os.system("docker build . -t backend5")
os.system("docker tag backend5 kubregistry1.azurecr.io/backend5:latest")
os.system("docker push kubregistry1.azurecr.io/backend5:latest")