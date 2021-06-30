#!/usr/bin/python3
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

lcd = CharLCD(pin_rs=7, pin_e=11, pins_data=[13, 15, 12, 16], numbering_mode=GPIO.BOARD)

lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string('Hello, World!')

#GPIO.cleanup()
