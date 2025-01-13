import os
os.system("docker build . -t backend3")
os.system("docker tag backend3 kubregistry1.azurecr.io/backend3:latest")
os.system("docker push kubregistry2.azurecr.io/backend3:latest")
