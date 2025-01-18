import os
os.system("docker build . -t backend")
os.system("docker tag backend kubregistry2.azurecr.io/backend:latest")
os.system("docker push kubregistry2.azurecr.io/backend:latest")