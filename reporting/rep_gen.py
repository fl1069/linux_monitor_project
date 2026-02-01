#!/usr/bin/env python3
import sys
import os
sys.path.append('..')
from system_monitoring import System_Monitoring as sm

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
