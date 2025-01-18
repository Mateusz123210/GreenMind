import os
os.system("docker build . -t backend2")
os.system("docker tag backend2 kubregistry2.azurecr.io/backend2:latest")
os.system("docker push kubregistry2.azurecr.io/backend2:latest")