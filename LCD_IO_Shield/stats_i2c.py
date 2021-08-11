#!/usr/bin/python3
# to install RPLCD, sudo pip3 install RPLCD
# for 16x2 I2C Character LCD Module

from RPLCD.i2c import CharLCD
import time
import subprocess
import threading

lcd = CharLCD('PCF8574', 0x3f)

def get_network_interface_state(interface):
    try:
        return subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[:-1]
    except:
        return 'down'

def get_ip_address(interface):
    if get_network_interface_state(interface) == 'down':
        return None
    cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
    try:
        return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]
    except:
        return None

def get_cpu_usage():
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    return CPU

def get_cpu_temp():
    cmd = "/opt/vc/bin/vcgencmd measure_temp"
    TEMP = subprocess.check_output(cmd, shell=True)
    return TEMP

def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as infile:
        return (f"{float(infile.read())*1e-3:4.1f}'C") 

def lcd_update_timer():
    threading.Timer(1.0, lcd_update_timer).start()
    #cmd = "free -m | awk 'NR==2{printf \"Mem:  %.0f%% %s/%s M\", $3*100/$2, $3,$2 }'"
    cmd = "free -m | awk 'NR==2{printf \"%.0f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3, $2, $5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"D:%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell=True) 
    cpuload = int(float(get_cpu_usage().decode())*100/4)
    
    if get_ip_address('wlan0') == None:
        interface = 'eth0'
    else:
        interface = 'wlan0'
    
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"{interface:<5}{cpu_temp():>7}{cpuload:>3}%"[0:16])

    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"{str(get_ip_address(interface)):<12}{MemUsage.decode():>4}"[0:16])
 
lcd.clear()
time.sleep(1.0)
lcd_update_timer()
