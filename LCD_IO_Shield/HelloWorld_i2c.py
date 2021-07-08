#!/usr/bin/python3
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x3f)

lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string('Hello, World!')
