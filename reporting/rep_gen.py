#!/usr/bin/env python3
import sys
import os
sys.path.append('..')
from system_monitoring import System_Monitoring as sm
from directory_monitor import dir_monitor as dm


report = "/home/aix/linux_monitor_project/reporting/report.txt"
if not os.path.exists(report):
       os.makedirs(os.path.dirname(report), exist_ok=True)

with open(report, 'w') as f:
     f.write("===SYSTEM REPORT===\n\n")
     f.write(f"cpu usage percentage:{sm.cpu_usage_percentage}\n")
     f.write(f"cpu load average:{sm.cpu_load_average1_5_15 }\n")
     f.write(f"Number of running process:{sm.running_process_count}\n\n")
     f.write(f"Total memory:{sm.memory_total/ (1024**3):.2f}GB\n")
     f.write(f"Total memory used:{sm.memory_used/ (1024**3):.2f}GB\n")
     f.write(f"Total memory available:{sm.memory_available/ (1024**3):.2f}GB\n")
     f.write(f"Memory usage percentage:{sm.memory_usage_percentage}\n")
     f.write(f"Disk total:{sm.disk.total/ (1024**3):.2f}GB\n")
     f.write(f"Disk used:{sm.disk.used/ (1024**3):.2f}GB\n")
     f.write(f"Disk free:{sm.disk.free/ (1024**3):.2f}GB\n")
     f.write(f"Disk usage percentage:{sm.disk.percent}\n")
     f.write(f"System uptime:{sm.uptime_seconds/3600:.2f} hours\n")
     f.write(f"System idle time:{sm.idle_second/3600:.2f} hours\n")
     f.write(f"Total processes:{sm.total_process}\n")
     f.write(f"Number of running vs sleeping processes:{sm.running_process_count}vs{sm.sleeping_process_count}\n")
     f.write(f"Top CPU process 1: PID:{sm.top_cpu[0][1]} {sm.top_cpu[0][2]} {sm.top_cpu[0][0]}%\n")
     f.write(f"Top CPU process 2: PID:{sm.top_cpu[1][1]} {sm.top_cpu[1][2]} {sm.top_cpu[1][0]}%\n")
     f.write(f"Top CPU process 3: PID:{sm.top_cpu[2][1]} {sm.top_cpu[2][2]} {sm.top_cpu[2][0]}%\n")
     f.write(f"Top Memory process 1: PID:{sm.top_mem[0][1]} {sm.top_mem[0][2]} {sm.top_mem[0][0]/ (1024**3):.2f}GB\n")
     f.write(f"Top Memory process 2: PID:{sm.top_mem[1][1]} {sm.top_mem[1][2]} {sm.top_mem[1][0]/ (1024**3):.2f}GB\n")
     f.write(f"Top Memory process 3: PID:{sm.top_mem[2][1]} {sm.top_mem[2][2]} {sm.top_mem[2][0]/ (1024**3):.2f}GB\n")
     f.write("\n--- DIRECTORY MONITORING ---\n")
     f.write(f"\nMonitored directory: {dm.monitor_directory}\n")
     f.write(f"Total files in directory: {dm.total_files}\n")
     f.write(f"Recent directory events:\n{dm.recent_logs}\n") 
     f.write("\n===END OF REPORT===\n")
