import os
os.system("docker build . -t backend4")
os.system("docker run -p 8006:8006 backend4")