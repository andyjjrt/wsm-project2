import os, subprocess

def buildIndex():
  result = subprocess.run(["sh", f"{os.path.dirname(__file__)}/buildIndex.sh"])
  
if __name__ == "__main__":
  buildIndex()