import os
os.system("docker build . -t backend2")
os.system("docker run -p 8000:8000 backend2")