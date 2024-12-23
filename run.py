import os
os.system("docker build . -t backend")
os.system("docker run -p 8005:8005 backend")