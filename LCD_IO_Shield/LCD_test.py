#!/usr/bin/python3
#sudo pip3 install RPLCD

import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

GPIO.setwarnings(False)
lcd = CharLCD(pin_rs=8, pin_rw=None, pin_e=11, pins_data=[13, 15, 12, 16],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string('Hello world')
