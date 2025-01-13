import os
os.system("docker build . -t frontend1")
os.system("docker tag frontend1 kubregistry2.azurecr.io/frontend1:latest")
os.system("docker push kubregistry2.azurecr.io/frontend1:latest")
