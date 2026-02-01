#!/usr/bin/env python3
import psutil #toolsssssssssssssssssssssssssssss

#log file loaction
log_file = "report/system_log.txt"

#cpu metrics
cpu_usage_percentage =( psutil.cpu_percent(interval=1.0,percpu=True))
cpu_load_average1_5_15 = psutil.getloadavg()
all_processes = list(psutil.process_iter())
running_process = []
for p in all_processes:
    try:
        if str(p.status()).lower() == 'running':
            running_process.append(p)
    except:
        continue

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

all_processes = list(psutil.process_iter())
top_cpu = sorted(
    [(p.cpu_percent(0.1), p.pid, p.name()) for p in all_processes[:80]],
    reverse=True
)[:3]

top_mem = sorted(
    [(p.memory_info().rss, p.pid, p.name()) for p in all_processes[:80]],
    reverse=True
)[:3]
