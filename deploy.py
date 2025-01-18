import os
os.system("docker build . -t backend9")
os.system("docker tag backend9 kubregistry2.azurecr.io/backend9:latest")
os.system("docker push kubregistry2.azurecr.io/backend9:latest")