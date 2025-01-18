import os
os.system("docker build . -t backend6")
os.system("docker tag backend6 kubregistry2.azurecr.io/backend6:latest")
os.system("docker push kubregistry2.azurecr.io/backend6:latest")