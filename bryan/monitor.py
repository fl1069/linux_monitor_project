# get system info (cpu, memory, disk, process)
import psutil

# used for timer
import time

# used to write csv file
import csv

# used to get current time
from datetime import datetime

# csv file loaction
log_file = "reports/system_log.csv"

# check if csv file exist
try:
    f = open(log_file, "r")   # try open file
    f.close()
except:
    # create csv file if not exist
    f = open(log_file, "w", newline="")
    writer = csv.writer(f)

    # write colum names
    writer.writerow([
        "time",
        "cpu",
        "memory",
        "disk",
        "process_total"
    ])

    f.close()

while True:
    # get current time in string
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # get cpu usage
    cpu = psutil.cpu_percent()

    # get memory usage
    memory = psutil.virtual_memory().percent

    # get disk usage
    disk = psutil.disk_usage("/").percent

    # get total process count
    process_total = len(psutil.pids())

    # open csv file to add new data
    f = open(log_file, "a", newline="")
    writer = csv.writer(f)

    # write one row into csv
    writer.writerow([
        current_time,
        cpu,
        memory,
        disk,
        process_total
    ])

    f.close()

    # show record time in terminal
    print("recorded at", current_time)

    # wait 10s
    time.sleep(10)
