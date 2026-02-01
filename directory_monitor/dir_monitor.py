#!/usr/bin/env python3
import os
import stat
import time
from datetime import datetime
from pathlib import Path

MONITOR_DIRECTORY = "./monitored_directory" #change to dir u want to monitor
previous_files = set(os.listdir(monitor_dir))
current_files = set(os.listdir(monitor_dir))
#File creation
new_files = current_files - previous_files
