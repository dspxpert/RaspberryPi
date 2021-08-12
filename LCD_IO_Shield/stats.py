#!/usr/bin/python3
# to install RPLCD, sudo pip3 install RPLCD

import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import time
import subprocess
import threading

# Hardkernel LCD+IO Shield Pin definition for RPi.GPIO GPIO.BOARD numbering mode
LCD_RS = 7
LCD_E  = 11
LCD_RW = None
LCD_D4 = 13
LCD_D5 = 15
LCD_D6 = 12
LCD_D7 = 16

LED1 = 29
LED2 = 31
LED3 = 33
LED4 = 35
LED7 = 26
LED6 = 32
LED5 = 36

SW1 = 18
SW2 = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup([LED1, LED2, LED3, LED4, LED5, LED6, LED7], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([SW1, SW2], GPIO.IN, pull_up_down=GPIO.PUD_UP)

#lcd = CharLCD(pin_rs=LCD_RS, pin_rw=LCD_RW, pin_e=LCD_E, pins_data=[LCD_D4, LCD_D5, LCD_D6, LCD_D7],
lcd = CharLCD(pin_rs=LCD_RS, pin_e=LCD_E, pins_data=[LCD_D4, LCD_D5, LCD_D6, LCD_D7],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

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

LED1_state = 0
LED2_state = 0
LED5_state = 0
button1_prev = 1
button2_prev = 1

lcd.clear()
time.sleep(1.0)
lcd_update_timer()

while True:    
    button1 = GPIO.input(SW1)
    button2 = GPIO.input(SW2)
    if button1 == 0 and button2 == 0:
        threading.Timer(1.0, lcd_update_timer).cancel()
        time.sleep(1.5)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED5, GPIO.LOW)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('System Poweroff.')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('Good Bye!')
        subprecess.check_output('sudo poweroff', shell=True)
        break

    if button1 == 0 and button1_prev == 1:
        LED1_state ^=1
        GPIO.output(LED1, LED1_state)
    button1_prev = button1    

    if button2 == 0 and button2_prev == 1:
        LED2_state ^=1
        GPIO.output(LED2, LED2_state)
    button2_prev = button2

    LED5_state ^=1
    GPIO.output(LED5, LED5_state)
    time.sleep(0.1)

GPIO.cleanup()
