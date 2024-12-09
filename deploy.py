import os
os.system("docker build . -t backend2")
os.system("docker tag backend2 thingssensorsservice.azurecr.io/backend2:latest")
os.system("docker push thingssensorsservice.azurecr.io/backend2:latest")