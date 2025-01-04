import os
os.system("docker build . -t backend")
os.system("docker tag backend kubregistry1.azurecr.io/backend:latest")
os.system("docker push kubregistry1.azurecr.io/backend:latest")