# Configuration Backup Tool for VISIT
# Developed by Dineshkumar Rajendran

import json
import shutil
import os
from datetime import datetime

def backup_config():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"config_backup_{timestamp}.json"
ECHO is off.
    try:
        if os.path.exists("../app/config.json"):
            shutil.copy("../app/config.json", f"../backup/{backup_name}")
            print(f"Configuration backed up as {backup_name}")
        else:
            print("No configuration file found to backup")
    except Exception as e:
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    backup_config()
