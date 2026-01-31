import psutil #toolsssssssssssssssssssssssssssss

#log file loaction
log_file = "report/system_log.txt"

#cpu metrics
cpu_usage_percentage = psutil.cpu_percent(percpu=True)
cpu_load_average1_5_15 = psutil.getloadavg()
running_process =[]
for p in psutil.process_iter():
          if p.status() == psutil.STATUS_RUNNING:
             running_process.append(p)
running_process_count = len(running_process)
#memory metrics
memory = psutil.virtual_memory() #all information of memory
memory_total = memory.total
memory_used = memory.used
memory_available = memory.available
memory_usage_percentage = memory.percent
#disk metrics
disk = psutil.disk_usage('/') #this include everthing and need to choose path(root)
#system uptime(using proc this time 11111111111111)(a file in root record memory and uptime info)
with open('/proc/uptime','r') as f:
    uptime_seconds,idle_second = map(float,f.read().split())
#active process
total_process = len(psutil.pids())
sleeping_process =[]
for p in psutil.process_iter():
          if p.status() == psutil.STATUS_SLEEPING:
             sleeping_process.append(p)
sleeping_process_count = len(sleeping_process)

with open(log_file,'w') as f:
     f.write(str(cpu_usage_percentage))
