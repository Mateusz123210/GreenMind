import os
os.system("docker build . -t backend")
os.system("docker tag backend greenmind.azurecr.io/backend:latest")
os.system("docker push greenmind.azurecr.io/backend:latest")