import os
os.system("docker build . -t backend3")
os.system("docker run -p 8004:8004 backend3")