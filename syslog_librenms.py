import random
import time
import datetime
import socket

# Config
FLUENTD_HOST = '127.0.0.1'  # Change to Fluentd IP if remote
FLUENTD_PORT = 514

# Data definitions
devices = ["router1", "switch1", "firewall1", "server1", "server2"]
log_levels = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFORMATIONAL", "DEBUG"]
messages = [
    "Interface eth0 is down", "Reboot detected", "High CPU usage", 
    "Disk space running low", "Configuration change detected",
    "SNMP timeout", "BGP session reset", "Temperature sensor alert"
]
severities = list(range(8))

# Syslog entry generator
def generate_log_entry():
    timestamp = datetime.datetime.now().strftime("%b %d %H:%M:%S")
    hostname = random.choice(devices)
    severity = random.choice(severities)
    log_level = log_levels[severity]
    facility = random.randint(0, 15)
    message = random.choice(messages)
    return f"<{facility*8+severity}>{timestamp} {hostname} LibreNMS: [{log_level}] {message}"

# Log sender
def send_logs(num_entries=50, interval=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for _ in range(num_entries):
        log_entry = generate_log_entry()
        print(log_entry)  # Optional: show on console
        sock.sendto(log_entry.encode(), (FLUENTD_HOST, FLUENTD_PORT))
        time.sleep(interval)
    sock.close()

if __name__ == "__main__":
    send_logs()

