import os
os.system("docker build . -t backend2")
os.system("docker tag backend2 kubregistry1.azurecr.io/backend2:latest")
os.system("docker push kubregistry1.azurecr.io/backend2:latest")