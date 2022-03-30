import psutil
import json
import os
import subprocess

def get_network_name():

# Get network name
  #net=str(os.system("iwgetid"))
  net = subprocess.getoutput("iwgetid")

  length = len(net)
  data = net[17:length-1]
  return data

def get_cpu():

# Get cpu statistics
  cpu = str(psutil.cpu_percent()) + '%'


  data = str(cpu)
  return data


def get_memory():

# Calculate memory information
  memory = psutil.virtual_memory()
# Convert Bytes to MB (Bytes -> KB -> MB)
  available = round(memory.available/1024.0/1024.0,1)
  total = round(memory.total/1024.0/1024.0,1)
  mem_info = str(available) + '/' + str(total) + '('+ str(memory.percent) + '%)'


  data = str(mem_info)
  return data

def get_hdd():

# Calculate disk information
  disk = psutil.disk_usage('/')
# Convert Bytes to GB (Bytes -> KB -> MB -> GB)
  free = round(disk.free/1024.0/1024.0/1024.0,1)
  total = round(disk.total/1024.0/1024.0/1024.0,1)
  disk_info = str(free) + '/' + str(total) + 'GB(' + str(disk.percent) + '%)'


  data = str(disk_info)
  return data

def get_revision():
#find model from revision
  models =  '{"0002":"Model B Rev 1","0003":"Model B Rev 1","0004":"Model B Rev 2", "0005":"Model B Rev 2", "0006":"Model B Rev 2","0007":"Model A","0008":"Model A","0009":"Model A","000d":"Model A","000e":"Model A","000f":"Model A","0010":"Model B+","0013":"Model B+","900032":"Model B+","0011":"Compute Module","0014":"Compute Module","0012":"Model A+","a01041 (Sony, UK)":"Pi 2 Model B v1.1","a21041 (Embest, China)":"Pi 2 Model B v1.1","a22042":"Pi 2 Model B v1.2","900092":"Pi Zero v1.2","900093":"Pi Zero v1.3","9000c1":"Pi Zero W","a02082 (Sony, UK)":"Pi 3 Model B","a22082 (Embest, China)":"Pi 3 Model B","a020d3 (Sony, UK)":"Pi 3 Model B+","a03111 (Sony, UK)":"Pi 4","b03111 (Sony, UK)":"Pi 4","b03112 (Sony, UK)":"Pi 4","b03114 (Sony, UK)":"Pi 4","c03111 (Sony, UK)":"Pi 4","c03112 (Sony, UK)":"Pi 4","c03114 (Sony, UK)":"Pi 4","d03114 (Sony, UK)":"Pi 4","c03130 (Sony, UK)":"Pi 400","902120 (Sony, UK)":"Pi Zero 2 W"}'
  models_json = json.loads(models)
  

  # Extract board revision from cpuinfo file
  myrevision = "0000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:5]=='Model':
        length=len(line)
        myrevision = line[9:length-1]
    f.close()
  except:
    myrevision = "0000"
  
  data = str(myrevision[:20]) 

  #for key in models_json:
    #print(key,":",data)
    #if key == data:
      #print (models_json[key])
      #data = models_json[key]

  return data


print(json.dumps(get_network_name()))

