import psutil
from datetime import datetime

class Power:

    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if not cpu:
            self.cpu_percent = psutil.cpu_percent(interval=0.1)
        if not ram_total:
            self.ram_total = psutil.virtual_memory().total
        if not ram_used:
            self.ram_used = psutil.virtual_memory().used
        if not timestamp:
            self.timestamp = datetime.now()

    def __str__(self):
        ram_used_gb = self.ram_used / (1024 ** 3)
        ram_total_gb = self.ram_total / (1024 ** 3)
        return (f"CPU: {self.cpu_percent}% | "
                f"RAM: {ram_used_gb:.2f}GB / {ram_total_gb:.2f}GB")