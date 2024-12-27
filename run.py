import os
os.system("docker build . -t backend11")
os.system("docker run -p 8008:8008 backend11")