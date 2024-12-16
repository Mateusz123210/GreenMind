import os
os.system("docker build . -t backend6")
os.system("docker run -p 8002:8002 backend6")