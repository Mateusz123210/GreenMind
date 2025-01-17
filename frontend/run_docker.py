import os
os.system("docker build . -t frontend1")
os.system("docker run -p 3000:3000 frontend1")