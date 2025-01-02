import os

os.system("kubectl delete pods --all --all-namespaces")
os.system("kubectl delete services --all --all-namespaces")
os.system("kubectl delete deployments --all --all-namespaces")
os.system("kubectl delete ingress --all --all-namespaces")