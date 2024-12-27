import os
os.system("docker build . -t backend5")
os.system("docker run -p 8007:8007 backend5")