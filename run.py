import os
os.system("docker build . -t backend9")
os.system("docker run -p 8001:8001 backend9")