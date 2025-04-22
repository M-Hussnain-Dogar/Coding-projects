import psutil
import platform
import socket
import cpuinfo
import os
import time
import json
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer

html_file = "full_system_report.html"
json_file = "system_data.json"

# Function to fetch system information
def get_system_info():
    cpu_data = cpuinfo.get_cpu_info()
    return {
        "OS": f"{platform.system()} {platform.release()}",
        "OS Version": platform.version(),
        "Hostname": socket.gethostname(),
        "Machine Type": platform.machine(),
        "Processor": cpu_data["brand_raw"],
        "Architecture": cpu_data["arch"],
        "CPU Cores (Physical)": psutil.cpu_count(logical=False),
        "CPU Cores (Logical)": psutil.cpu_count(logical=True),
        "Max Frequency (MHz)": psutil.cpu_freq().max,
        "Current Frequency (MHz)": psutil.cpu_freq().current,
        "Total CPU Usage (%)": psutil.cpu_percent(interval=1),  # Fix: CPU update interval
    }

# Get Memory Info
def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "Total RAM (GB)": round(memory.total / (1024**3), 2),
        "Available RAM (GB)": round(memory.available / (1024**3), 2),
        "Used RAM (GB)": round(memory.used / (1024**3), 2),
        "Memory Usage (%)": memory.percent,
    }

# Get Disk Info
def get_disk_info():
    disk_data = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_data.append({
                "Device": partition.device,
                "Mount Point": partition.mountpoint,
                "Total Space (GB)": round(usage.total / (1024**3), 2),
                "Used Space (GB)": round(usage.used / (1024**3), 2),
                "Free Space (GB)": round(usage.free / (1024**3), 2),
                "Usage (%)": usage.percent
            })
        except PermissionError:
            pass  # Ignore inaccessible partitions
    return disk_data

# Get GPU Info (Windows only)
def get_gpu_info():
    if os.name == "nt":
        try:
            gpu_output = subprocess.check_output("wmic path win32_VideoController get Name", shell=True).decode()
            gpus = [line.strip() for line in gpu_output.split("\n") if line.strip()]
            return gpus[1] if len(gpus) > 1 else "GPU info unavailable"
        except:
            return "GPU info unavailable"
    return "N/A"

# Get CPU Temperature (Windows)
def get_cpu_temp():
    if os.name == "nt":
        try:
            temp_output = subprocess.check_output(
                "wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature",
                shell=True
            ).decode().split("\n")
            temp_values = [line.strip() for line in temp_output if line.strip().isdigit()]
            return round((int(temp_values[0]) / 10) - 273.15, 2) if temp_values else "Temperature unavailable"
        except:
            return "Temperature unavailable"
    return "N/A"

# Serve HTML & JSON files
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = f"/{html_file}"
        elif self.path == "/system_data.json":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            with open(json_file, "r") as file:
                self.wfile.write(file.read().encode())
            return
        return SimpleHTTPRequestHandler.do_GET(self)

# Start web server
def start_server():
    httpd = HTTPServer(("localhost", 8080), MyHandler)
    print("✅ Server running on http://localhost:8080")
    httpd.serve_forever()

# Function to update JSON file every second
def update_json():
    while True:
        data = {
            "system_info": get_system_info(),
            "memory_info": get_memory_info(),
            "disk_info": get_disk_info(),
            "cpu_usage_per_core": psutil.cpu_percent(percpu=True, interval=1),
            "gpu_info": get_gpu_info(),
            "cpu_temp": get_cpu_temp(),
        }

        # Write to JSON file
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)

        print(f"✅ System report updated in '{json_file}'")
        time.sleep(0.5)

# Run update function & server in parallel
import threading
threading.Thread(target=update_json, daemon=True).start()
start_server()
