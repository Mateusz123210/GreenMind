import os

base_path = os.getcwd()

next_path = os.path.join(base_path, "analysisService/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "authenticationService/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "dataQuering/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "oldDataRemover/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "plantManagement/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "schedulerService/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "sensorsService/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")

next_path = os.path.join(base_path, "weatherApiService/GreenMind/")
os.chdir(next_path)
os.system("python deploy.py")