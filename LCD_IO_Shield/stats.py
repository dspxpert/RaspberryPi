#!/usr/bin/python3
#sudo pip3 install RPLCD

import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import time
import subprocess

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

# Return a string representing the percentage of CPU in use

def get_cpu_usage():
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    return CPU

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
lcd.clear()
'''
lcd.cursor_pos = (0, 0)
lcd.write_string('Hello world')
'''

while True:
    #cmd = "free -m | awk 'NR==2{printf \"Mem:  %.0f%% %s/%s M\", $3*100/$2, $3,$2 }'"
    cmd = "free -m | awk 'NR==2{printf \"%.0f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3, $2, $5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"D:%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell=True) 

    cpuload = int(float(get_cpu_usage().decode())*100/4)
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"{str(get_ip_address('eth0')):<12}{cpuload:>3}%")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"{str(get_ip_address('wlan1')):<12}{MemUsage.decode():>4}")
    #print(f"{str(get_ip_address('eth0')):<12}{cpuload:>3}%")
    #print(f"{str(get_ip_address('wlan1')):<12}{MemUsage.decode():>4}")
    
    button1 = GPIO.input(SW1)
    button2 = GPIO.input(SW2)
    if button1 == 0:
        print('button1 pressed')
        GPIO.output(LED1, GPIO.HIGH)
    else:
        GPIO.output(LED1, GPIO.LOW)
    if button2 == 0:
        print('button2 pressed')
        break    

    time.sleep(0.25)

GPIO.cleanup() 
