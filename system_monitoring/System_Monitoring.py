#!/usr/bin/env python3
import psutil
import time
import os
from datetime import datetime
from pathlib import Path

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Define log file path in reporting directory
log_file = os.path.join(project_root, "reporting", "system_monitor_log.txt")

def log_system_event(event_type, data=None):
    """Log system monitoring events"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {event_type}\n")
            if data:
                if isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"  {key}: {value}\n")
                else:
                    f.write(f"  {data}\n")
            f.write("-" * 40 + "\n")
        print(f"System log: {event_type}")
    except Exception as e:
        print(f"Failed to write system log: {e}")

# CPU metrics
cpu_usage_percentage = psutil.cpu_percent(interval=1.0, percpu=True)
cpu_load_average1_5_15 = psutil.getloadavg()

# Log CPU data
log_system_event("CPU_METRICS", {
    "cpu_usage": cpu_usage_percentage,
    "load_average": cpu_load_average1_5_15
})

# Process monitoring
all_processes = list(psutil.process_iter())
running_process = []
for p in all_processes:
    try:
        if str(p.status()).lower() == 'running':
            running_process.append(p)
    except:
        continue

running_process_count = len(running_process)

# Memory metrics
memory = psutil.virtual_memory()
memory_total = memory.total
memory_used = memory.used
memory_available = memory.available
memory_usage_percentage = memory.percent

# Log memory data
log_system_event("MEMORY_METRICS", {
    "total_gb": f"{memory_total / (1024**3):.2f} GB",
    "used_gb": f"{memory_used / (1024**3):.2f} GB",
    "available_gb": f"{memory_available / (1024**3):.2f} GB",
    "usage_percent": f"{memory_usage_percentage}%"
})

# Disk metrics
disk = psutil.disk_usage('/')

# Log disk data
log_system_event("DISK_METRICS", {
    "total_gb": f"{disk.total / (1024**3):.2f} GB",
    "used_gb": f"{disk.used / (1024**3):.2f} GB",
    "free_gb": f"{disk.free / (1024**3):.2f} GB",
    "usage_percent": f"{disk.percent}%"
})

# System uptime from /proc/uptime
try:
    with open('/proc/uptime', 'r') as f:
        uptime_seconds, idle_second = map(float, f.read().split())
    
    # Log uptime
    log_system_event("SYSTEM_UPTIME", {
        "uptime_hours": f"{uptime_seconds / 3600:.2f}",
        "idle_hours": f"{idle_second / 3600:.2f}"
    })
except Exception as e:
    uptime_seconds, idle_second = 0, 0
    log_system_event("UPTIME_ERROR", str(e))

# Active process statistics
total_process = len(psutil.pids())

sleeping_process = []
for p in psutil.process_iter():
    try:
        if p.status() == psutil.STATUS_SLEEPING:
            sleeping_process.append(p)
    except:
        continue

sleeping_process_count = len(sleeping_process)

# Log process data
log_system_event("PROCESS_METRICS", {
    "total_processes": total_process,
    "running_processes": running_process_count,
    "sleeping_processes": sleeping_process_count
})

# Top CPU and Memory processes
# Need to initialize CPU usage for accurate measurement
for p in all_processes[:80]:
    try:
        p.cpu_percent(interval=None)
    except:
        pass

time.sleep(0.2)

top_cpu = sorted(
    [(p.cpu_percent(interval=None), p.pid, p.name()) for p in all_processes[:80]],
    reverse=True
)[:3]

top_mem = sorted(
    [(p.memory_info().rss, p.pid, p.name()) for p in all_processes[:80]],
    reverse=True
)[:3]

# Log top processes
log_system_event("TOP_CPU_PROCESSES", [
    f"PID:{pid} {name} {cpu:.1f}%" for cpu, pid, name in top_cpu
])

log_system_event("TOP_MEMORY_PROCESSES", [
    f"PID:{pid} {name} {mem / (1024**3):.2f} GB" for mem, pid, name in top_mem
])

# Export all variables for use in other modules
__all__ = [
    'cpu_usage_percentage',
    'cpu_load_average1_5_15',
    'running_process_count',
    'memory_total',
    'memory_used',
    'memory_available',
    'memory_usage_percentage',
    'disk',
    'uptime_seconds',
    'idle_second',
    'total_process',
    'sleeping_process_count',
    'top_cpu',
    'top_mem',
    'log_system_event'
]

# Log completion
log_system_event("SYSTEM_MONITORING_COMPLETED", f"Collected all metrics at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
