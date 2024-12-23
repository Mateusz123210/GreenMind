import os
os.system("docker build . -t backend2")
os.system("docker run -p 8003:8003 backend2")