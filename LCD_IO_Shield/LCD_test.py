#!/usr/bin/python3
#sudo pip3 install RPLCD

LCD_RS = 8
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


import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup([LED1, LED2, LED3, LED4, LED5, LED6, LED7], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([SW1, SW1], GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = CharLCD(pin_rs=LCD_RS, pin_rw=LCD_RW, pin_e=LCD_E, pins_data=[LCD_D4, LCD_D5, LCD_D6, LCD_D7],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string('Hello world')

try:
    while True:
        button1 = GPIO.input(SW1)
        button2 = GPIO.input(SW1)
        if button1 == 0:
            GPIO.output(LED1, GPIO.HIGH)
        else:
            GPIO.output(LED1, GPIO.LOW)
        if button2 == 0:
            break    
finally:
    GPIO.cleanup()

GPIO.cleanup()
