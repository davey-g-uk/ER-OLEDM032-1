import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(25,GPIO.OUT) # 25 RESET (low to reset)
GPIO.output(25,True)    #    Release the RESET

GPIO.setup(24,GPIO.OUT)   # 24 D/C

def resetOLED():
    GPIO.output(25,False) # Activate reset
    time.sleep(0.5 )      # Hold it low for half a second
    GPIO.output(25,True)  # Release reset
    time.sleep(1.0)       # Give the chip a second to come up
 
# Using spidev for SPI
#   
import spidev
#
spi = spidev.SpiDev()
spi.open(0,0)
spi.cshigh = False   # CS active low
spi.lsbfirst = False # Send MSB first
spi.mode = 3         # Clock idle high, data on 2nd edge (end of pulse)
spi.max_speed_hz = 5000000  

# mode 00 ... clock idle low,  data valid at beginning of pulse (low to high)
# mode 01 ... clock idle low,  data valid at end of pulse (high to low)
# mode 10 ... clock idle high, data valid at beginning of pulse (high to low)
# mode 11 ... clock idle high, data valid at end of pulse (low to high)
#
def Write_Instruction(dataByte):
    GPIO.output(24,False) # Select command register
    spi.writebytes([dataByte])
#    
def Write_Data(dataByte):
    GPIO.output(24,True) # Select data register
    spi.writebytes([dataByte])    


"""
# Bit-banging the SPI port
#
GPIO.setup(10,GPIO.OUT) # 10 MOSI
#
GPIO.setup(11,GPIO.OUT) # 11 SCLK
GPIO.output(11,True)    #    Clock is idle-high
#
GPIO.setup(8,GPIO.OUT)  #  8 Chip Select (active low)
GPIO.output(8,False)    #    Select the chip
#
def Write_Instruction(dataByte):
    GPIO.output(24,False) # Select command register
    for x in xrange(8):
        GPIO.output(10, (dataByte&0x80)!=0)    
        GPIO.output(11, False)
        dataByte = dataByte << 1
        GPIO.output(11, True)   
#
def Write_Data(dataByte):
    GPIO.output(24,True) # Select data register
    for x in xrange(8):
        GPIO.output(10, (dataByte&0x80)!=0)    
        GPIO.output(11, False)
        dataByte = dataByte << 1
        GPIO.output(11, True)
"""        

# http://www.buydisplay.com/default/oled-3-2-inch-displays-module-companies-with-driver-circuit-blue-on-black
    
# Translated from C to Python
#
# ER-OLEDM032-1_DemoCode.c
#
# EASTRISING TECHNOLOGY CO,.LTD.//
# Module    : ER-OLEDM032-1Series  3.12"  YELLOW/BLUE/GREEN  256*64 dots
# Lanuage   : C51 Code
# Create    : JAVEN
# Date      : May-1-2013
# Drive IC  : SSD1332U
# INTERFACE : 8BIT 8080
# MCU       : AT89LV52
# VBAT      : 3.3-5VV    VDD:regulated internally from VCI 

Contrast_level=0x80

numberImages = [  
    0x00,0x00,0x00,0x18,0x24,0x42,0x42,0x42,0x42,0x42,0x42,0x24,0x18,0x00,0x00,0x00, # 0
    0x00,0x00,0x00,0x10,0x70,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00,0x00, # 1
    0x00,0x00,0x00,0x3C,0x42,0x42,0x02,0x04,0x08,0x10,0x20,0x42,0x7E,0x00,0x00,0x00, # 2
    0x00,0x00,0x00,0x3C,0x42,0x42,0x04,0x18,0x04,0x02,0x42,0x42,0x3C,0x00,0x00,0x00, # 3
    0x00,0x00,0x00,0x08,0x08,0x18,0x28,0x48,0x48,0x7E,0x08,0x08,0x1E,0x00,0x00,0x00, # 4
    0x00,0x00,0x00,0x7E,0x40,0x40,0x5C,0x62,0x02,0x02,0x42,0x42,0x3C,0x00,0x00,0x00, # 5
    0x00,0x00,0x00,0x1C,0x24,0x40,0x40,0x5C,0x62,0x42,0x42,0x42,0x3C,0x00,0x00,0x00, # 6
    0x00,0x00,0x00,0x7E,0x44,0x44,0x08,0x08,0x10,0x10,0x10,0x10,0x10,0x00,0x00,0x00, # 7
    0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x3C,0x24,0x42,0x42,0x42,0x3C,0x00,0x00,0x00, # 8
    0x00,0x00,0x00,0x38,0x44,0x42,0x42,0x46,0x3A,0x02,0x02,0x24,0x38,0x00,0x00,0x00, # 9
]

asciiImages = [
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # SPACE
    0x00,0x00,0x00,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x00,0x00,0x18,0x18,0x00,0x00, # !
    0x00,0x00,0x00,0x00,0x00,0x00,0x14,0x28,0x28,0x50,0x00,0x00,0x00,0x00,0x00,0x00, # "
    0x00,0x00,0x00,0x14,0x14,0x7E,0x14,0x14,0x28,0x7E,0x28,0x28,0x28,0x00,0x00,0x00, # #
    0x00,0x00,0x10,0x38,0x54,0x54,0x50,0x30,0x18,0x14,0x54,0x54,0x38,0x10,0x10,0x00, # $
    0x00,0x00,0x00,0x44,0xA4,0xA8,0xA8,0x50,0x14,0x2A,0x2A,0x4A,0x44,0x00,0x00,0x00, # %
    0x00,0x00,0x00,0x20,0x50,0x50,0x50,0x7C,0xA8,0xA8,0x98,0x88,0x76,0x00,0x00,0x00, # &
    0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x08,0x30,0x00,0x00,0x00,0x00,0x00,0x00, # '
    0x00,0x00,0x04,0x08,0x10,0x10,0x20,0x20,0x20,0x20,0x20,0x10,0x10,0x08,0x04,0x00, # (
    0x00,0x00,0x20,0x10,0x08,0x08,0x04,0x04,0x04,0x04,0x04,0x08,0x08,0x10,0x20,0x00, # )
    0x00,0x00,0x00,0x00,0x10,0x10,0xD6,0x38,0x38,0xD6,0x10,0x10,0x00,0x00,0x00,0x00, # *
    0x00,0x00,0x00,0x00,0x00,0x10,0x10,0x10,0xFE,0x10,0x10,0x10,0x00,0x00,0x00,0x00, # +
    0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x08,0x30,0x00,0x00,0x00,0x00,0x00,0x00, # ,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFE,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # -
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # .
    0x00,0x00,0x02,0x04,0x04,0x04,0x08,0x08,0x10,0x10,0x10,0x20,0x20,0x40,0x40,0x00, # /
    
    0x00,0x00,0x00,0x18,0x24,0x42,0x42,0x42,0x42,0x42,0x42,0x24,0x18,0x00,0x00,0x00, # 0
    0x00,0x00,0x00,0x10,0x70,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00,0x00, # 1
    0x00,0x00,0x00,0x3C,0x42,0x42,0x02,0x04,0x08,0x10,0x20,0x42,0x7E,0x00,0x00,0x00, # 2
    0x00,0x00,0x00,0x3C,0x42,0x42,0x04,0x18,0x04,0x02,0x42,0x42,0x3C,0x00,0x00,0x00, # 3
    0x00,0x00,0x00,0x08,0x08,0x18,0x28,0x48,0x48,0x7E,0x08,0x08,0x1E,0x00,0x00,0x00, # 4
    0x00,0x00,0x00,0x7E,0x40,0x40,0x5C,0x62,0x02,0x02,0x42,0x42,0x3C,0x00,0x00,0x00, # 5
    0x00,0x00,0x00,0x1C,0x24,0x40,0x40,0x5C,0x62,0x42,0x42,0x42,0x3C,0x00,0x00,0x00, # 6
    0x00,0x00,0x00,0x7E,0x44,0x44,0x08,0x08,0x10,0x10,0x10,0x10,0x10,0x00,0x00,0x00, # 7
    0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x3C,0x24,0x42,0x42,0x42,0x3C,0x00,0x00,0x00, # 8
    0x00,0x00,0x00,0x38,0x44,0x42,0x42,0x46,0x3A,0x02,0x02,0x24,0x38,0x00,0x00,0x00, # 9
    
    0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00,0x00, # :
    0x00,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x08,0x08,0x10,0x00,0x00,0x00, # ;
    0x00,0x00,0x00,0x02,0x04,0x08,0x10,0x20,0x40,0x20,0x10,0x08,0x04,0x02,0x00,0x00, # <
    0x00,0x00,0x00,0x00,0x00,0x00,0xFE,0x00,0x00,0xFE,0x00,0x00,0x00,0x00,0x00,0x00, # =
    0x00,0x00,0x00,0x40,0x20,0x10,0x08,0x04,0x02,0x04,0x08,0x10,0x20,0x40,0x00,0x00, # >
    0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x02,0x04,0x08,0x08,0x00,0x18,0x18,0x00,0x00, # ?
    0x00,0x00,0x00,0x38,0x44,0x9A,0xAA,0xAA,0xAA,0xAA,0xB4,0x42,0x3C,0x00,0x00,0x00, # @
    
    
    0x00,0x00,0x00,0x10,0x10,0x28,0x28,0x28,0x28,0x7C,0x44,0x44,0xEE,0x00,0x00,0x00, # A
    0x00,0x00,0x00,0xFC,0x42,0x42,0x44,0x78,0x44,0x42,0x42,0x42,0xFC,0x00,0x00,0x00, # B
    0x00,0x00,0x00,0x3E,0x42,0x82,0x80,0x80,0x80,0x80,0x82,0x44,0x38,0x00,0x00,0x00, # C
    0x00,0x00,0x00,0xF8,0x44,0x42,0x42,0x42,0x42,0x42,0x42,0x44,0xF8,0x00,0x00,0x00, # D
    0x00,0x00,0x00,0xFC,0x42,0x48,0x48,0x78,0x48,0x48,0x40,0x42,0xFC,0x00,0x00,0x00, # E
    0x00,0x00,0x00,0xFC,0x42,0x48,0x48,0x78,0x48,0x48,0x40,0x40,0xE0,0x00,0x00,0x00, # F
    0x00,0x00,0x00,0x3C,0x44,0x84,0x80,0x80,0x80,0x8E,0x84,0x44,0x38,0x00,0x00,0x00, # G
    0x00,0x00,0x00,0xEE,0x44,0x44,0x44,0x7C,0x44,0x44,0x44,0x44,0xEE,0x00,0x00,0x00, # H
    0x00,0x00,0x00,0x7C,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00,0x00, # I
    0x00,0x00,0x3E,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x88,0xF0,0x00,0x00, # J
    0x00,0x00,0x00,0xEE,0x44,0x48,0x50,0x70,0x50,0x48,0x48,0x44,0xEE,0x00,0x00,0x00, # K
    0x00,0x00,0x00,0xE0,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x42,0xFE,0x00,0x00,0x00, # L
    0x00,0x00,0x00,0xEE,0x6C,0x6C,0x6C,0x54,0x54,0x54,0x54,0x54,0xD6,0x00,0x00,0x00, # M
    0x00,0x00,0x00,0xEE,0x64,0x64,0x54,0x54,0x54,0x4C,0x4C,0x4C,0xE4,0x00,0x00,0x00, # N
    0x00,0x00,0x00,0x38,0x44,0x82,0x82,0x82,0x82,0x82,0x82,0x44,0x38,0x00,0x00,0x00, # O
    0x00,0x00,0x00,0xFC,0x42,0x42,0x42,0x7C,0x40,0x40,0x40,0x40,0xE0,0x00,0x00,0x00, # P
    0x00,0x00,0x00,0x38,0x44,0x82,0x82,0x82,0x82,0x82,0xB2,0x4C,0x38,0x06,0x00,0x00, # Q
    0x00,0x00,0x00,0xF8,0x44,0x44,0x44,0x78,0x50,0x48,0x48,0x44,0xE6,0x00,0x00,0x00, # R
    0x00,0x00,0x00,0x3E,0x42,0x42,0x40,0x30,0x0C,0x02,0x42,0x42,0x7C,0x00,0x00,0x00, # S
    0x00,0x00,0x00,0xFE,0x92,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x38,0x00,0x00,0x00, # T
    0x00,0x00,0x00,0xEE,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x44,0x38,0x00,0x00,0x00, # U
    0x00,0x00,0x00,0xEE,0x44,0x44,0x44,0x28,0x28,0x28,0x28,0x10,0x10,0x00,0x00,0x00, # V
    0x00,0x00,0x00,0xD6,0x54,0x54,0x54,0x54,0x6C,0x28,0x28,0x28,0x28,0x00,0x00,0x00, # W
    0x00,0x00,0x00,0xEE,0x44,0x28,0x28,0x10,0x10,0x28,0x28,0x44,0xEE,0x00,0x00,0x00, # X
    0x00,0x00,0x00,0xEE,0x44,0x44,0x28,0x28,0x10,0x10,0x10,0x10,0x38,0x00,0x00,0x00, # Y
    0x00,0x00,0x00,0x3E,0x44,0x04,0x08,0x08,0x10,0x10,0x20,0x22,0x7E,0x00,0x00,0x00, # Z
    
    0x00,0x00,0x3C,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x3C,0x00, # [
    0x00,0x00,0x40,0x40,0x20,0x20,0x10,0x10,0x10,0x08,0x08,0x04,0x04,0x04,0x02,0x00, # BACK-SLASH
    0x00,0x00,0x3C,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x3C,0x00, # ]
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x24,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # ^
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFE,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # _
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x30,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # `
    
    0x00,0x00,0x00,0x00,0x00,0x38,0x44,0x1C,0x24,0x44,0x44,0x3E,0x00,0x00,0x00,0x00, # a
    0x00,0x00,0x00,0xC0,0x40,0x40,0x5C,0x62,0x42,0x42,0x42,0x42,0x7C,0x00,0x00,0x00, # b
    0x00,0x00,0x00,0x00,0x00,0x1C,0x22,0x40,0x40,0x40,0x22,0x1C,0x00,0x00,0x00,0x00, # c
    0x00,0x00,0x00,0x0C,0x04,0x04,0x7C,0x84,0x84,0x84,0x84,0x8C,0x76,0x00,0x00,0x00, # d
    0x00,0x00,0x00,0x00,0x00,0x3C,0x42,0x7E,0x40,0x40,0x42,0x3C,0x00,0x00,0x00,0x00, # e
    0x00,0x00,0x00,0x0E,0x12,0x10,0x7C,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00,0x00, # f
    0x00,0x00,0x00,0x00,0x3E,0x44,0x44,0x38,0x40,0x3C,0x42,0x42,0x3C,0x00,0x00,0x00, # g
    0x00,0x00,0x00,0xC0,0x40,0x40,0x5C,0x62,0x42,0x42,0x42,0x42,0xE7,0x00,0x00,0x00, # h
    0x00,0x00,0x00,0x30,0x30,0x00,0x70,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00,0x00, # i
    0x00,0x00,0x0C,0x0C,0x00,0x1C,0x04,0x04,0x04,0x04,0x04,0x04,0x44,0x78,0x00,0x00, # j
    0x00,0x00,0x00,0xC0,0x40,0x40,0x4E,0x48,0x50,0x68,0x48,0x44,0xEE,0x00,0x00,0x00, # k
    0x00,0x00,0x00,0x70,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00,0x00, # l
    0x00,0x00,0x00,0x00,0x00,0xF8,0x54,0x54,0x54,0x54,0x54,0xD6,0x00,0x00,0x00,0x00, # m
    0x00,0x00,0x00,0x00,0x00,0xDC,0x62,0x42,0x42,0x42,0x42,0xE7,0x00,0x00,0x00,0x00, # n
    0x00,0x00,0x00,0x00,0x00,0x18,0x24,0x42,0x42,0x42,0x24,0x18,0x00,0x00,0x00,0x00, # o
    0x00,0x00,0x00,0x00,0xDC,0x62,0x42,0x42,0x42,0x42,0x7C,0x40,0xE0,0x00,0x00,0x00, # p
    0x00,0x00,0x00,0x00,0x7C,0x84,0x84,0x84,0x84,0x8C,0x74,0x04,0x0E,0x00,0x00,0x00, # q
    0x00,0x00,0x00,0x00,0x00,0xEE,0x32,0x20,0x20,0x20,0x20,0xF8,0x00,0x00,0x00,0x00, # r
    0x00,0x00,0x00,0x00,0x00,0x3C,0x44,0x40,0x38,0x04,0x44,0x78,0x00,0x00,0x00,0x00, # s
    0x00,0x00,0x00,0x00,0x10,0x10,0x7C,0x10,0x10,0x10,0x10,0x10,0x0C,0x00,0x00,0x00, # t
    0x00,0x00,0x00,0x00,0x00,0xC6,0x42,0x42,0x42,0x42,0x46,0x3B,0x00,0x00,0x00,0x00, # u
    0x00,0x00,0x00,0x00,0x00,0xE7,0x42,0x24,0x24,0x28,0x10,0x10,0x00,0x00,0x00,0x00, # v
    0x00,0x00,0x00,0x00,0x00,0xD6,0x54,0x54,0x54,0x28,0x28,0x28,0x00,0x00,0x00,0x00, # w
    0x00,0x00,0x00,0x00,0x00,0x6E,0x24,0x18,0x18,0x18,0x24,0x76,0x00,0x00,0x00,0x00, # x
    0x00,0x00,0x00,0x00,0xE7,0x42,0x24,0x24,0x28,0x18,0x10,0x10,0xE0,0x00,0x00,0x00, # y
    0x00,0x00,0x00,0x00,0x00,0x7E,0x44,0x08,0x10,0x10,0x22,0x7E,0x00,0x00,0x00,0x00, # z
]

specialChars = [
0x10,0x00,0x10,0xFC,0x10,0x84,0x10,0x84,0xFC,0x84,0x14,0xFC,0x14,0x84,0x14,0x84,
0x14,0x84,0x24,0x84,0x24,0xFC,0x24,0x00,0x44,0x02,0x44,0x02,0x83,0xFE,0x00,0x00,

0x00,0x00,0x1F,0xF0,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x1F,0xF0,0x10,0x10,
0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x1F,0xF0,0x10,0x10,0x00,0x00,0x00,0x00,

0x02,0x00,0x02,0x00,0x7F,0xFC,0x04,0x00,0x08,0x80,0x08,0x80,0x10,0x80,0x1F,0xF8,
0x00,0x80,0x08,0xA0,0x0C,0x90,0x18,0x88,0x10,0x8C,0x22,0x84,0x01,0x80,0x00,0x80,

0x02,0x00,0x01,0x00,0x00,0x80,0xFF,0xFE,0x02,0x00,0x02,0x00,0x03,0xF0,0x02,0x10,
0x04,0x10,0x04,0x10,0x08,0x10,0x08,0x10,0x10,0x10,0x20,0x90,0xC0,0x60,0x00,0x00,
]

pic1 = [
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x04,0x00,0x00,0x00,0x00,
0x01,0x00,0x00,0x00,0x00,0x10,0x08,0x40,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x01,0xE0,0x00,0x00,0x00,0x00,0x20,0xF8,0x08,0x04,0x04,0x00,0x00,0x00,
0x01,0x00,0x01,0x00,0x03,0x10,0x08,0x40,0x01,0x00,0x0D,0xF0,0x01,0x00,0x07,0xF1,
0x80,0x00,0x01,0xE0,0x00,0x00,0x00,0x00,0x13,0x08,0x08,0x84,0x04,0x00,0x03,0xE0,
0x01,0x70,0x00,0x80,0x1C,0x10,0x08,0x40,0x01,0xFC,0x35,0x10,0x00,0x80,0x00,0x11,
0x80,0x00,0x03,0xE4,0x00,0x00,0x00,0x00,0x04,0xA0,0x08,0xA4,0x07,0x3C,0x0C,0x20,
0x1F,0x80,0x00,0x00,0x04,0x50,0x08,0x78,0x3E,0x00,0x29,0xD0,0x04,0x40,0x03,0x11,
0x80,0x00,0x07,0xEF,0xC0,0x00,0x00,0x00,0x41,0x10,0x08,0xA4,0x3D,0x44,0x08,0x20,
0x02,0x00,0x00,0xFC,0x07,0x10,0x0E,0xC0,0x02,0x00,0x29,0x20,0x04,0x40,0x1C,0x11,
0x80,0x00,0x0F,0xEF,0xFE,0x00,0x00,0x00,0x22,0x80,0x0C,0xA4,0x05,0x74,0x08,0x20,
0x02,0x80,0x3F,0x80,0x1C,0x50,0x38,0x40,0x03,0xE0,0x25,0xE0,0x08,0x20,0x00,0x11,
0x80,0x00,0x0F,0xE7,0xFF,0xE0,0x00,0x00,0x00,0xF8,0x38,0xA4,0x05,0x44,0x0F,0xA0,
0x04,0x80,0x01,0x00,0x66,0x10,0x08,0x70,0x06,0x20,0x3D,0x08,0x09,0x18,0x07,0x11,
0x80,0x00,0x07,0xE7,0x3F,0xFE,0x00,0x00,0x17,0x80,0x08,0xA4,0x09,0x44,0x08,0x20,
0x09,0xF0,0x01,0xE0,0x0D,0x3E,0x0D,0x90,0x0B,0xA0,0x21,0x90,0x11,0x0E,0x19,0x11,
0x80,0x00,0x07,0xE7,0x07,0xFF,0xF0,0x00,0x11,0xC0,0x0E,0xA4,0x09,0x78,0x08,0x20,
0x0E,0x80,0x02,0x20,0x14,0xD0,0x18,0xA0,0x12,0x20,0x21,0x60,0x22,0x00,0x11,0x11,
0x80,0x00,0x07,0xE7,0x00,0xFF,0xFE,0x00,0x22,0xA0,0x19,0x24,0x11,0x02,0x08,0x20,
0x00,0x90,0x04,0x20,0x24,0x10,0x68,0x40,0x22,0x20,0x21,0x20,0x04,0x40,0x1F,0x11,
0x80,0x00,0x07,0xF7,0x00,0x1F,0xFE,0x00,0x24,0x98,0x61,0x24,0x21,0x02,0x0F,0xE0,
0x08,0x88,0x08,0x20,0x04,0x10,0x08,0xA0,0x43,0xA0,0x21,0x5E,0x09,0xE0,0x10,0x11,
0x80,0x00,0x03,0xF7,0x00,0x03,0xFE,0x00,0x28,0x8E,0x02,0x04,0x41,0x02,0x00,0x20,
0x08,0x84,0x31,0x40,0x04,0x10,0x0B,0x18,0x02,0x20,0x21,0x80,0x0E,0x20,0x00,0x11,
0x80,0x00,0x03,0xF7,0x00,0x00,0x7E,0x00,0x00,0x80,0x04,0x04,0x00,0xFC,0x00,0x00,
0x11,0x80,0x00,0x80,0x04,0x10,0x18,0x0E,0x04,0x60,0x21,0x00,0x00,0x00,0x00,0x71,
0x80,0x00,0x03,0xF3,0x00,0x00,0x1C,0x00,0x00,0x80,0x00,0x04,0x00,0x00,0x00,0x00,
0x00,0x80,0x00,0x00,0x00,0x10,0x00,0x00,0x04,0x20,0x00,0x00,0x00,0x00,0x00,0x21,
0x80,0x00,0x01,0xF3,0x00,0x00,0x1C,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0xC0,0x01,0xF3,0x80,0x00,0x1C,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0xF8,0x01,0xF3,0x80,0x00,0x3C,0x00,0x0F,0x30,0x00,0x01,0xFB,0x00,0x00,0x03,
0xE0,0x00,0x27,0xCC,0x03,0x00,0x00,0x3F,0x00,0x03,0x00,0x00,0x18,0x00,0x00,0x01,
0x80,0x7F,0x00,0xF3,0x80,0x00,0x3C,0x00,0x19,0xB0,0x00,0x00,0x1B,0x00,0x00,0x03,
0x00,0x00,0x66,0x60,0x00,0x00,0x00,0x0C,0x00,0x03,0x00,0x00,0x18,0x00,0x00,0x01,
0x80,0x7F,0xC0,0xF3,0x80,0x00,0x38,0x00,0x18,0x3E,0x3C,0xF8,0x33,0xE3,0xCF,0x83,
0x07,0x1E,0xF6,0x6C,0xF3,0x7C,0x7C,0x0C,0x3C,0x73,0xE7,0xC7,0x99,0xE3,0xF8,0xC1,
0x80,0x3F,0xF8,0xF3,0x80,0x00,0x38,0x00,0x1E,0x33,0x66,0xCC,0x63,0x36,0x6C,0xC3,
0xE9,0xB3,0x66,0x6D,0x9B,0x66,0xCC,0x0C,0x66,0xDB,0x36,0x6C,0xDB,0x36,0x6D,0x81,
0x80,0x3F,0xFE,0xF9,0x80,0x00,0x38,0x00,0x07,0xB3,0x7E,0xCC,0x63,0x37,0xEC,0xC3,
0x07,0xBC,0x67,0xCD,0xE3,0x66,0xCC,0x0C,0x7E,0xC3,0x36,0x6C,0xDB,0x36,0x6D,0x81,
0x80,0x1D,0xFF,0x79,0x80,0x00,0x78,0x00,0x01,0xB3,0x60,0xCC,0xC3,0x36,0x0C,0xC3,
0x0D,0x8F,0x66,0xCC,0x7B,0x66,0xCC,0x0C,0x60,0xC3,0x36,0x6C,0xDB,0x36,0x6D,0x81,
0x80,0x1C,0x3F,0x79,0x80,0x00,0x70,0x00,0x19,0xB3,0x66,0xCD,0x83,0x36,0x6C,0xC3,
0x0D,0xB3,0x66,0x6D,0x9B,0x66,0xCC,0x0C,0x66,0xDB,0x36,0x6C,0xDB,0x36,0x67,0x01,
0x80,0x1C,0x07,0x79,0x80,0x00,0x70,0x00,0x0F,0x33,0x3C,0xCD,0xFB,0x33,0xCC,0xC3,
0xE7,0x9E,0x36,0x3C,0xF3,0x66,0x7C,0x0C,0x3C,0x73,0x36,0x67,0x99,0xE3,0xE7,0x01,
0x80,0x0E,0x00,0x39,0x80,0x00,0x70,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x8C,0x00,0x00,0x00,0x00,0x00,0x00,0x04,0x66,0x01,
0x80,0x0E,0x00,0x39,0xC0,0x00,0x70,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x78,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0xDC,0x01,
0x80,0x06,0x00,0x39,0xC0,0x00,0x60,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x07,0x00,0x18,0xC0,0x00,0xE0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x03,0x00,0x18,0xC0,0x00,0xE0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x03,0x00,0x1C,0xC0,0x00,0xE0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x01,0x80,0x1C,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x01,0x80,0x0C,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x00,0x00,0x1F,0xE7,0xF8,0x00,
0xF0,0x60,0x3F,0xCF,0xC1,0xC1,0xC7,0x0F,0x87,0x80,0x0C,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x80,0x0C,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x00,0x00,0x1F,0xE7,0xFC,0x03,
0xFC,0x60,0x3F,0xCF,0xF1,0xC1,0xCF,0x9F,0xCF,0xC0,0x1C,0x00,0x00,0x00,0x33,0x01,
0x80,0x00,0x80,0x0C,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x06,0x0C,0x03,
0x0C,0x60,0x30,0x0C,0x31,0xE3,0xDD,0xD8,0xD8,0xC0,0x3C,0x00,0x00,0x00,0x33,0x01,
0x80,0x00,0x00,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x06,0x0C,0x06,
0x06,0x60,0x30,0x0C,0x19,0xE3,0xD8,0xC0,0xD8,0xC0,0x6C,0x0E,0x03,0x1C,0x33,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0xE6,0x0C,0x06,
0x06,0x60,0x3F,0xCC,0x19,0xA2,0xD8,0xC3,0x80,0xC0,0x4C,0x1B,0x07,0x36,0x44,0x01,
0x87,0xE0,0x00,0x02,0x3F,0x0C,0x00,0xC0,0x00,0x00,0x00,0x00,0x1F,0xE7,0xF8,0x06,
0x06,0x60,0x3F,0xCC,0x19,0xB6,0xD8,0xC3,0x81,0x80,0x0C,0x03,0x0F,0x06,0x00,0x01,
0x86,0x00,0x00,0x06,0x31,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x07,0xF0,0xF6,
0x06,0x60,0x30,0x0C,0x19,0xB6,0xD8,0xC0,0xC3,0x0F,0x0C,0x06,0x0B,0x06,0x00,0x01,
0x86,0x03,0xC3,0xCF,0x31,0x8C,0x78,0xCD,0x86,0xC0,0x00,0x00,0x18,0x06,0x38,0xF6,
0x06,0x60,0x30,0x0C,0x19,0x9C,0xD8,0xD8,0xC6,0x0F,0x0C,0x03,0x03,0x0C,0x00,0x01,
0x86,0x04,0x66,0x66,0x31,0x8C,0xCC,0xCE,0xCD,0xC0,0x00,0x00,0x18,0x06,0x1C,0x03,
0x0C,0x60,0x30,0x0C,0x31,0x9C,0xDD,0xDC,0xCC,0x00,0x0C,0x03,0x03,0x18,0x00,0x01,
0x87,0xE1,0xE7,0x06,0x3F,0x0C,0xE0,0xCC,0xCC,0xC0,0x00,0x00,0x1F,0xE6,0x0C,0x03,
0xFC,0x7F,0x3F,0xCF,0xF1,0x9C,0xCF,0x8F,0x9F,0xC0,0x0C,0x1B,0x63,0x30,0x00,0x01,
0x86,0x03,0x63,0xC6,0x33,0x0C,0x78,0xCC,0xCC,0xC0,0x00,0x00,0x1F,0xE6,0x0E,0x00,
0xF0,0x7F,0x3F,0xCF,0xC1,0x88,0xC7,0x07,0x1F,0xC0,0x0C,0x0E,0x63,0x3E,0x00,0x01,
0x86,0x06,0x60,0xE6,0x31,0x8C,0x1C,0xCC,0xCC,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x86,0x06,0x66,0x66,0x31,0x8C,0xCC,0xCC,0xCD,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x87,0xE3,0xE3,0xC3,0x30,0xCC,0x78,0xCC,0xC6,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x08,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x07,0x80,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0xBF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0xBF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0xC7,0x9C,0x47,0x04,0x3C,
0x01,0x00,0x04,0x38,0x38,0x00,0x00,0x00,0x00,0x00,0x14,0x04,0x5E,0x00,0x10,0x11,
0xA0,0x00,0x00,0x28,0x00,0x20,0x00,0x00,0x00,0x00,0x02,0x24,0x22,0xE8,0x8C,0x22,
0x01,0x00,0x0C,0x44,0x44,0x00,0x00,0x00,0x00,0x00,0x14,0x04,0x61,0x00,0x00,0x11,
0xA0,0x00,0x00,0x20,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x28,0x20,0x48,0x14,0x21,
0x3B,0x9C,0x14,0x40,0x82,0xA7,0x22,0x05,0x8E,0x53,0x94,0xE4,0xA0,0x39,0x53,0x91,
0xBC,0x8A,0x21,0xE8,0xEF,0x27,0x22,0x18,0xE7,0x60,0x00,0x2F,0x3C,0xAF,0x14,0x21,
0x45,0x22,0x04,0x78,0x80,0xC8,0xA2,0x06,0x51,0x64,0x55,0x14,0x98,0x45,0x94,0x51,
0xA2,0x89,0x42,0x29,0x08,0xA0,0x94,0x25,0x14,0x90,0x00,0x40,0xA2,0x08,0xA4,0x21,
0x45,0x18,0x04,0x44,0x8E,0x87,0x94,0x04,0x4F,0x43,0xD5,0xF4,0x86,0x7D,0x13,0xD1,
0xA2,0x89,0x5A,0x28,0xC8,0xA3,0x94,0x21,0x14,0x90,0x00,0x80,0xA2,0x08,0xBE,0x21,
0x45,0x04,0x04,0x44,0x82,0x88,0x94,0x04,0x51,0x44,0x55,0x04,0x81,0x41,0x14,0x51,
0xA2,0x89,0x42,0x28,0x28,0xA4,0x94,0x25,0x14,0x90,0x01,0x08,0xA2,0x08,0x84,0x22,
0x45,0x22,0x04,0x44,0x44,0x89,0x88,0x06,0x53,0x44,0xD5,0x15,0x21,0x45,0x14,0xD1,
0xBC,0x78,0x81,0xE9,0xCF,0x23,0x88,0x98,0xE4,0x90,0x03,0xE7,0x1C,0x07,0x04,0x3C,
0x39,0x9C,0x04,0x38,0x38,0x86,0x88,0x05,0x8D,0x43,0x54,0xE5,0x1E,0x39,0x13,0x51,
0x80,0x00,0x80,0x00,0x08,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x08,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x03,0x00,0x00,0x08,0x00,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x10,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
]

pic2 = [
0xFC,0x00,0x00,0x20,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7F,
0x80,0x00,0x00,0xFE,0x00,0x00,0x00,0x0C,0x00,0x0C,0x07,0x00,0x00,0x00,0x00,0x00,
0x00,0x7B,0xE0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0xE0,0x00,0x01,
0x80,0x00,0x39,0xBE,0x1E,0x00,0x00,0x1C,0x00,0x3E,0x0F,0xFF,0x80,0x00,0x00,0x00,
0x01,0xFF,0x7E,0x00,0x00,0x00,0x0F,0x82,0x78,0x00,0x00,0x00,0x07,0xF0,0x00,0x01,
0x80,0x01,0xFF,0x07,0x3F,0xF8,0x00,0x3C,0x00,0x7F,0x3E,0x73,0x80,0x00,0x00,0x00,
0x03,0xFC,0x1F,0x00,0x00,0x00,0x1F,0xCF,0xD8,0x00,0x00,0x00,0x1F,0xF8,0x00,0x01,
0x80,0x07,0x82,0x03,0x3F,0xF8,0x00,0x3C,0x00,0xFF,0xE0,0x03,0x00,0x00,0x00,0x00,
0x07,0xFC,0x01,0x80,0x00,0x00,0x3F,0xD8,0x30,0x00,0x00,0x00,0x1F,0xF8,0x00,0x01,
0x80,0x03,0x00,0x1F,0xFF,0xF8,0x00,0x3E,0x01,0xFF,0xC0,0x01,0x80,0x00,0x00,0x00,
0x07,0xFC,0x00,0xC0,0x00,0x00,0x3F,0xE0,0x0C,0x00,0x00,0x00,0x3F,0xF8,0x00,0x01,
0x00,0x03,0x00,0x7E,0x7F,0xF8,0x00,0x7E,0x01,0xFF,0xE0,0x01,0xC3,0xC0,0x00,0x00,
0x07,0xFC,0x00,0x80,0x00,0x00,0x7F,0xE0,0x06,0x00,0x00,0x00,0x3F,0xF8,0x10,0x01,
0x00,0x03,0x7F,0xFF,0x7F,0xFC,0x00,0x7E,0x03,0xFF,0xC0,0x01,0xEF,0xE0,0x00,0x00,
0x07,0xEF,0xFB,0x80,0x00,0x00,0x7F,0xF8,0x04,0x00,0x00,0x00,0x3F,0xF8,0xF8,0x00,
0x00,0x03,0xF7,0xFF,0xFF,0xFE,0x00,0xEE,0x03,0xFF,0xE0,0x01,0xFF,0xE0,0x00,0x00,
0x07,0xFF,0xFF,0xC0,0x00,0x00,0x7F,0xCF,0xFE,0x00,0x00,0x00,0x3F,0xF1,0xDC,0x00,
0x00,0x07,0xFE,0x7F,0x3F,0xFE,0x00,0xB2,0x03,0xFF,0xF8,0x03,0x1F,0xF0,0x00,0x00,
0x07,0xFF,0xE1,0xB0,0x00,0x00,0x3F,0x83,0xFE,0x00,0x00,0x00,0x3F,0xF3,0x86,0x00,
0x07,0xCF,0xFC,0x1E,0x1F,0xFF,0x01,0xFA,0x01,0xFF,0x1C,0x7F,0xDF,0xF0,0x00,0x00,
0x0C,0xFB,0xFE,0xD8,0x00,0x00,0x3F,0x03,0xFD,0x00,0x00,0x00,0x1F,0x1F,0x03,0x80,
0x07,0xFF,0xF8,0x07,0xCF,0xFF,0x83,0xCF,0x01,0xFF,0xEF,0xF8,0xEF,0xF0,0x00,0x00,
0x18,0x03,0xFF,0xCD,0xE0,0x00,0x60,0x03,0xFD,0x00,0x00,0x00,0x18,0x1F,0xC1,0x90,
0x1F,0xFB,0xE0,0x1F,0xF7,0xFF,0x0F,0xEF,0x00,0xEF,0xF7,0xFF,0xEF,0xF0,0x00,0x00,
0x1F,0x81,0xFF,0x07,0xF0,0x00,0xC0,0x03,0xFF,0x00,0x00,0x00,0x30,0x1F,0x60,0xF8,
0x1F,0xF8,0x38,0x1F,0xFF,0xFE,0x0F,0xFF,0x00,0x4F,0xFC,0xFF,0xE7,0xE0,0x00,0x00,
0x3F,0x80,0xFE,0x07,0xF8,0x01,0x80,0x01,0xFE,0x80,0x00,0x00,0x60,0x1F,0xB0,0x78,
0x1F,0xF0,0xFE,0x39,0xFF,0xFE,0x00,0x03,0x00,0x4F,0xFC,0xFF,0xE3,0xE0,0x00,0x00,
0x70,0x80,0xF8,0x07,0xF8,0x01,0x00,0x00,0xFC,0x80,0x00,0x00,0xC0,0x1F,0xD8,0x7C,
0x1F,0xF1,0xFF,0x30,0x7F,0xFC,0x00,0x01,0x80,0x83,0xF8,0x7F,0xE3,0xC0,0x00,0x01,
0xE3,0x03,0xF8,0x07,0xF8,0x02,0x00,0x00,0x20,0x80,0x00,0x01,0x80,0xDF,0xEC,0x7C,
0x1F,0xE3,0xF3,0x30,0x7F,0xFC,0x00,0x01,0x81,0x83,0xE0,0x3F,0xC2,0x00,0x00,0x03,
0x67,0x06,0x3C,0x03,0xF8,0x06,0x00,0x00,0x0E,0xC0,0x00,0x03,0x03,0xFF,0xFC,0xFC,
0x1F,0xE3,0xC1,0x26,0x3F,0xF8,0x00,0x00,0x81,0x0F,0xC0,0x06,0x02,0x00,0x00,0x06,
0x66,0x06,0x3C,0x03,0xF8,0x04,0x00,0x00,0x1F,0x40,0x00,0x06,0x07,0xFF,0xFD,0xFC,
0x07,0xE7,0xC1,0x2B,0x3F,0xF8,0x00,0x00,0xC3,0x3F,0xE0,0x38,0x03,0x00,0x00,0x0C,
0x6E,0x0E,0x3C,0x03,0xF8,0x0C,0x00,0x00,0x3F,0x40,0x00,0x04,0x0F,0xFF,0xEF,0xFC,
0x03,0xE7,0x9E,0x08,0x3F,0xF8,0x00,0x00,0xFF,0x7F,0xE0,0xFE,0x03,0x00,0x00,0x18,
0x30,0x1E,0x3C,0x03,0xF0,0x08,0x00,0x00,0x39,0xC0,0x00,0x0C,0x1F,0xFF,0xF7,0xF8,
0x00,0x67,0x92,0x00,0x7F,0xF8,0x00,0x00,0xC6,0xFC,0xE0,0xFF,0x83,0x00,0x00,0x10,
0x0E,0x1C,0x3C,0x03,0xF0,0x10,0x00,0x00,0x70,0x60,0x00,0x18,0x3F,0x9C,0x07,0xB0,
0x00,0x67,0x90,0x01,0xFD,0xF8,0x00,0x01,0xE7,0xFB,0xE1,0xFF,0xC3,0x00,0x00,0x30,
0x0F,0x18,0x7C,0x03,0xC0,0x10,0x00,0x00,0x73,0x20,0x00,0x30,0x3F,0x0C,0x07,0xF0,
0x00,0x67,0x82,0x01,0xF9,0xF8,0x00,0x03,0x7D,0xFE,0xC1,0xCF,0xC3,0x00,0x00,0x32,
0x00,0x18,0xFC,0x06,0x00,0x30,0x00,0x00,0x73,0x20,0x00,0x20,0x3E,0x04,0x03,0xF0,
0x00,0x67,0xC6,0x70,0x01,0xF8,0x00,0x02,0x3D,0xFC,0xC1,0xEF,0xC2,0x00,0x00,0x33,
0x00,0x0F,0xF8,0x06,0x00,0x20,0x00,0x00,0x33,0x30,0x00,0x60,0x3E,0x1C,0x03,0xE0,
0x00,0x67,0xFC,0xF0,0x01,0xF8,0x00,0x02,0x3D,0xF9,0x01,0x2F,0xE3,0x00,0x00,0x31,
0x08,0x07,0xF0,0x06,0x00,0x20,0x00,0x00,0x3B,0x18,0x00,0x40,0x3E,0x38,0x07,0xC0,
0x00,0x67,0xF8,0x23,0x01,0xF8,0x00,0x03,0x1D,0xFF,0x00,0x0F,0xC3,0x00,0x00,0x30,
0xFC,0x01,0xC0,0x04,0x00,0x60,0x00,0x00,0x3C,0x18,0x00,0x40,0x3E,0x38,0x0F,0x80,
0x00,0x63,0xF0,0x33,0x01,0xF8,0x00,0x01,0x8C,0xFF,0xC0,0xFF,0xC3,0x00,0x04,0x10,
0x64,0x00,0x00,0x04,0x00,0xE0,0x00,0x00,0x0C,0x08,0x00,0x60,0x1E,0x30,0x1F,0x80,
0x00,0x60,0x01,0xFE,0x01,0xF8,0x00,0x01,0xDC,0x7D,0xC0,0xFF,0xC3,0x00,0x0E,0x18,
0x06,0x00,0x00,0x0C,0x00,0xC0,0x00,0x00,0x00,0x08,0x00,0x60,0x0F,0x80,0x33,0x00,
0x00,0x60,0x01,0xC0,0x01,0xF8,0x00,0x00,0xFC,0x00,0x80,0x3F,0x83,0x00,0x1F,0x08,
0x03,0x00,0x00,0x0C,0x00,0xC0,0x00,0x00,0x00,0x18,0x00,0x20,0x33,0x80,0x73,0x00,
0x00,0x60,0x00,0x00,0x01,0xF8,0x00,0x00,0x1E,0x00,0x00,0x0E,0x06,0x00,0x3F,0x0C,
0x01,0x80,0x18,0x08,0x00,0xC0,0x00,0x00,0x00,0x50,0x00,0x30,0x18,0x00,0x63,0x00,
0x00,0x60,0x00,0x00,0x03,0xF8,0x00,0x00,0x0F,0x00,0x00,0x00,0x0E,0x00,0x7F,0xE6,
0x00,0xE0,0x70,0x08,0x00,0x60,0x00,0x00,0x00,0xD0,0x00,0x10,0x08,0x02,0x67,0x00,
0x00,0x60,0x00,0x00,0x03,0xF8,0x00,0x00,0x05,0x87,0xF0,0x00,0x0C,0x00,0xFF,0xFA,
0x00,0x3F,0xC0,0x18,0x00,0x20,0x00,0x00,0x00,0xB0,0x00,0x78,0x04,0x03,0x0E,0x00,
0x00,0x60,0x00,0x00,0x07,0xF8,0x00,0x00,0x06,0xC3,0xE0,0x00,0x18,0x00,0xFF,0xFF,
0x00,0x00,0x00,0x10,0x00,0x30,0x00,0x00,0x01,0x60,0x01,0xFC,0x06,0x03,0x7E,0x00,
0x00,0x30,0x00,0x00,0x0F,0xF0,0x00,0x00,0x06,0x60,0x00,0x00,0x70,0x00,0xFC,0xFF,
0xC0,0x00,0x00,0x30,0x00,0x10,0x00,0x00,0x00,0xC0,0x01,0xFC,0x03,0x00,0x7E,0x00,
0x00,0x38,0x00,0x00,0x3F,0xF0,0x00,0x00,0x03,0x38,0x00,0x00,0xE0,0x00,0x7F,0x7F,
0xF0,0x00,0x00,0x60,0x00,0x0C,0x00,0x00,0x03,0x80,0x07,0xFE,0x00,0xF8,0x3A,0x00,
0x00,0x1C,0x00,0x00,0x67,0xF0,0x00,0x00,0x03,0x0E,0x00,0x03,0x80,0x00,0x7B,0x7F,
0xF8,0x00,0x01,0xC0,0x00,0x06,0x00,0x00,0x06,0x00,0x0F,0xFF,0x80,0x3C,0x02,0x00,
0x00,0x0F,0x80,0x01,0x81,0xF0,0x00,0x00,0x01,0x8F,0xF8,0xFF,0x80,0x00,0x73,0x7F,
0xFF,0x00,0x0F,0x80,0x00,0x01,0x83,0xC0,0x1C,0x00,0x1F,0xFF,0x80,0x07,0xC4,0x00,
0x00,0x01,0xFF,0xF8,0x00,0x70,0x00,0x00,0x01,0x9E,0x3F,0xFF,0xC0,0x00,0xF3,0x7F,
0xFF,0xFD,0xFC,0x00,0x00,0x00,0xF7,0xE0,0x70,0x00,0x1F,0xFF,0x00,0x03,0x8C,0x00,
0x00,0x00,0x1F,0xE0,0x00,0x60,0x00,0x00,0x00,0xDC,0x00,0x77,0xC0,0x00,0xE2,0xFF,
0xFF,0xFF,0xE0,0x00,0x00,0x00,0x7F,0xE3,0xC0,0x00,0x1F,0xFE,0x00,0x00,0x18,0x00,
0x00,0x00,0x0F,0x80,0x00,0x20,0x00,0x00,0x00,0xD8,0x00,0x63,0xC0,0x01,0xF6,0xFF,
0xFF,0xFF,0xE0,0x00,0x00,0x00,0xFF,0xF2,0xC0,0x00,0x1F,0xFE,0x06,0x00,0xF0,0x00,
0x00,0x00,0x1F,0x80,0x00,0x20,0x00,0x00,0x00,0x70,0x00,0x61,0xC0,0x01,0xDD,0xFF,
0xFF,0xFF,0xE0,0x00,0x00,0x01,0x5F,0xC0,0x40,0x00,0x3F,0xFC,0x03,0xFF,0x80,0x00,
0x00,0x00,0x3F,0x00,0x00,0x30,0x00,0x00,0x00,0x70,0x00,0x60,0xC0,0x07,0xE3,0xCF,
0xFF,0xFF,0xE0,0x00,0x00,0x03,0xDF,0xC0,0x40,0x00,0x3F,0xD0,0x03,0x80,0x00,0x00,
0x00,0x00,0x3F,0x00,0x00,0x30,0x00,0x00,0x00,0x20,0x00,0x70,0x40,0x07,0xFF,0x93,
0xFF,0xFF,0xE0,0x00,0x00,0x03,0xBF,0x80,0x60,0x00,0x3B,0x80,0x03,0x80,0x00,0x00,
0x00,0x00,0x7F,0x00,0x00,0x30,0x00,0x00,0x00,0x60,0x00,0x18,0x60,0x07,0xFF,0x03,
0xFF,0xFF,0xE0,0x00,0x00,0x03,0xFF,0x80,0x30,0x00,0x2B,0x00,0x07,0x80,0x00,0x00,
0x00,0x00,0x7F,0x80,0x00,0x10,0x00,0x00,0x00,0x60,0x00,0x08,0x30,0x01,0xFF,0x73,
0xFF,0xFF,0xC0,0x00,0x00,0x03,0xFF,0x00,0x3E,0x00,0x36,0x00,0x07,0xC0,0x00,0x00,
0x00,0x00,0x7F,0x80,0x00,0x10,0x00,0x00,0x00,0x60,0x00,0x0C,0x30,0x00,0xFF,0x1B,
0xFF,0xFF,0xC0,0x00,0x00,0x07,0xFF,0x00,0x3F,0x00,0x1C,0x00,0x07,0xE0,0x00,0x00,
0x00,0x00,0x7F,0x00,0x00,0x10,0x00,0x00,0x00,0x40,0x00,0x06,0x18,0x00,0x7F,0x8B,
0xF3,0xFF,0xC0,0x00,0x00,0x07,0xFE,0x00,0x3F,0x00,0x1C,0x00,0x07,0xF0,0x00,0x00,
0x00,0x00,0x3F,0x00,0x00,0x10,0x00,0x00,0x00,0x40,0x00,0x04,0x10,0x00,0x1F,0xC7,
0xF1,0xFF,0xC0,0x00,0x00,0x07,0xFE,0x00,0x3F,0x00,0x2C,0x00,0x0F,0xF8,0x00,0x00,
0x00,0x00,0x3F,0x00,0x00,0x10,0x00,0x00,0x00,0x40,0x00,0x04,0x10,0x00,0x03,0xFF,
0xE0,0xFF,0x80,0x00,0x00,0x07,0xFC,0x00,0x3F,0x00,0xC8,0x00,0x0F,0xFC,0x00,0x00,
0x00,0x00,0x1F,0x00,0x00,0x18,0x00,0x00,0x00,0x40,0x00,0x07,0x30,0x00,0x00,0xFF,
0xE0,0x7F,0x80,0x00,0x00,0x07,0xFC,0x00,0x3E,0x00,0xC8,0x00,0x0B,0xF8,0x00,0x00,
0x00,0x00,0x0E,0x00,0x00,0x18,0x00,0x00,0x00,0x40,0x00,0x03,0xE0,0x00,0x00,0xFF,
0xC0,0x1F,0x80,0x00,0x00,0x07,0xFC,0x00,0x3C,0x00,0xC8,0x00,0x1B,0xF8,0x00,0x00,
0x00,0x00,0x04,0x00,0x00,0x18,0x00,0x00,0x00,0x40,0x00,0x03,0xC0,0x00,0x00,0xC7,
0x80,0x0F,0x00,0x00,0x00,0x07,0xF8,0x00,0x20,0x00,0xC8,0x00,0x1B,0xF8,0x00,0x00,
0x00,0x00,0x0C,0x00,0x00,0x18,0x00,0x00,0x00,0x40,0x00,0x03,0x80,0x00,0x00,0x40,
0x00,0x08,0x00,0x00,0x00,0x03,0xF8,0x00,0x20,0x00,0xCC,0x00,0x13,0xF0,0x00,0x00,
0x00,0x00,0x0C,0x00,0x00,0x18,0x00,0x00,0x00,0x40,0x00,0x03,0x00,0x00,0x00,0x40,
0x00,0x18,0x00,0x00,0x00,0x01,0xC0,0x00,0x60,0x00,0xCC,0x01,0x30,0x00,0x00,0x00,
0x00,0x00,0x0C,0x00,0x00,0x10,0x00,0x00,0x00,0x00,0x30,0x00,0x00,0x03,0x60,0x00,
0x30,0x00,0x00,0x00,0x00,0x00,0xC0,0x00,0x60,0x00,0xE4,0x01,0x60,0x00,0x00,0x00,
0x00,0x00,0x0C,0x00,0x00,0x10,0x00,0x00,0x00,0x00,0x30,0x00,0x00,0x03,0x00,0x00,
0x30,0x00,0x00,0x00,0x00,0x00,0xB0,0x00,0x60,0x00,0x3C,0x00,0xC0,0x00,0x00,0x00,
0x00,0x00,0x08,0x00,0x00,0x10,0x64,0xD9,0x36,0x4C,0x3E,0x67,0x8C,0x1F,0x67,0x9F,
0x33,0xB1,0x87,0x1E,0x7F,0xC1,0x90,0x00,0x30,0x00,0x06,0x00,0x80,0x00,0x00,0x00,
0x00,0x00,0x08,0x06,0x00,0x10,0x6E,0xDB,0xB6,0xEC,0x33,0x66,0xD8,0x33,0x6C,0xD9,
0xB4,0xDB,0x0D,0xB3,0x66,0x61,0x18,0x00,0x10,0x00,0x02,0x00,0x80,0x00,0x00,0x01,
0x80,0x00,0x08,0x03,0xE0,0x30,0x6E,0xDB,0xB6,0xEC,0x33,0x66,0xD8,0x33,0x6F,0x19,
0xB3,0xDB,0x0C,0x33,0x66,0x61,0x0C,0x00,0x10,0x00,0x02,0x00,0x80,0x00,0x00,0x01,
0x80,0x00,0x08,0x02,0x40,0x20,0x3B,0x8E,0xE3,0xB8,0x33,0x66,0xDB,0xB3,0x63,0xD9,
0xB6,0xDB,0x0C,0x33,0x66,0x61,0x87,0x00,0x10,0x00,0x02,0x01,0x80,0x00,0x00,0x01,
0x80,0x00,0x0C,0x06,0x40,0x20,0x3B,0x8E,0xE3,0xB9,0xB3,0x66,0x70,0x33,0x6C,0xD9,
0xB6,0xCE,0x6D,0xB3,0x66,0x60,0xC3,0xE0,0x20,0x00,0x03,0x03,0x00,0x00,0x00,0x01,
0x80,0x00,0x06,0x04,0x60,0xF8,0x31,0x8C,0x63,0x19,0xBE,0x3E,0x70,0x1F,0x67,0x9F,
0x33,0xCE,0x67,0x1E,0x66,0x60,0x61,0xE0,0x60,0x00,0x03,0x8E,0x00,0x00,0x00,0x01,
0x80,0x00,0x1F,0xFF,0xFF,0xF8,0x00,0x00,0x00,0x00,0x00,0x00,0x60,0x00,0x00,0x18,
0x00,0x0C,0x00,0x00,0x00,0x01,0x3F,0x31,0xC0,0x00,0x01,0xFC,0x00,0x00,0x00,0x01,
0xFC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0xC0,0x00,0x00,0x18,
0x00,0x38,0x00,0x00,0x00,0x00,0x1E,0x1F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7F,        
]
    
def Initial():    
    Write_Instruction(0xFD) # Set Command Lock
    
    Write_Instruction(0xFD) # SET COMMAND LOCK 
    Write_Data(0x12) # UNLOCK 
    Write_Instruction(0xAE) # DISPLAY OFF 
    Write_Instruction(0xB3) # DISPLAYDIVIDE CLOCKRADIO/OSCILLATAR FREQUANCY*/ 
    Write_Data(0x91) 
    Write_Instruction(0xCA) # multiplex ratio 
    Write_Data(0x3F) # duty = 1/64 
    Write_Instruction(0xA2) # set offset 
    Write_Data(0x00)
    Write_Instruction(0xA1) # start line 
    Write_Data(0x00)
    Write_Instruction(0xA0) #set remap
    Write_Data(0x14)
    Write_Data(0x11)
    
    Write_Instruction(0xAB) # funtion selection 
    Write_Data(0x01) # selection external vdd  
    Write_Instruction(0xB4)
    Write_Data(0xA0)
    Write_Data(0xfd) 
    Write_Instruction(0xC1) # set contrast current  
    Write_Data(Contrast_level)
    Write_Instruction(0xC7) # master contrast current control 
    Write_Data(0x0f)
     
    Write_Instruction(0xB1) # SET PHASE LENGTH
    Write_Data(0xE2)
    Write_Instruction(0xD1)
    Write_Data(0x82)
    Write_Data(0x20) 
    Write_Instruction(0xBB) # SET PRE-CHANGE VOLTAGE 
    Write_Data(0x1F)
    Write_Instruction(0xB6) # SET SECOND PRE-CHARGE PERIOD
    Write_Data(0x08)
    Write_Instruction(0xBE) # SET VCOMH  
    Write_Data(0x07)
    Write_Instruction(0xA6) # normal display 
    Clear_ram()
    Write_Instruction(0xAF) # display ON

def Clear_ram():
    Write_Instruction(0x15) 
    Write_Data(0x00)
    Write_Data(0x77) 
    Write_Instruction(0x75) 
    Write_Data(0x00)
    Write_Data(0x7f) 
    Write_Instruction(0x5C)    
    for y in xrange(128):
        for x in xrange(120):
            Write_Data(0x00)         

def Display_Picture(pic):
    Set_Row_Address(0)         
    Set_Column_Address(0)
    Write_Instruction(0x5c)    
    for i in xrange(64):
        for j in xrange(32):
            Data_processing(pic[i*32+j])

def Set_Row_Address(add):
    Write_Instruction(0x75) # SET SECOND PRE-CHARGE PERIOD 
    add = 0x3f & add
    Write_Data(add)
    Write_Data(0x3f)

def Set_Column_Address(add):
    add = 0x3f & add
    Write_Instruction(0x15) # SET SECOND PRE-CHARGE PERIOD  
    Write_Data(0x1c+add)
    Write_Data(0x5b)
    
def Data_processing(temp): # turns 1byte B/W data to 4 bye gray data
        temp1=temp&0x80
        temp2=(temp&0x40)>>3
        temp3=(temp&0x20)<<2
        temp4=(temp&0x10)>>1
        temp5=(temp&0x08)<<4
        temp6=(temp&0x04)<<1
        temp7=(temp&0x02)<<6
        temp8=(temp&0x01)<<3
        h11=temp1|(temp1>>1)|(temp1>>2)|(temp1>>3)
        h12=temp2|(temp2>>1)|(temp2>>2)|(temp2>>3)
        h13=temp3|(temp3>>1)|(temp3>>2)|(temp3>>3)
        h14=temp4|(temp4>>1)|(temp4>>2)|(temp4>>3)
        h15=temp5|(temp5>>1)|(temp5>>2)|(temp5>>3)
        h16=temp6|(temp6>>1)|(temp6>>2)|(temp6>>3)
        h17=temp7|(temp7>>1)|(temp7>>2)|(temp7>>3)
        h18=temp8|(temp8>>1)|(temp8>>2)|(temp8>>3)
        d1=h11|h12
        d2=h13|h14
        d3=h15|h16
        d4=h17|h18

        Write_Data(d1)
        Write_Data(d2)
        Write_Data(d3)
        Write_Data(d4)

def Write_number(value, column):
    for i in xrange(16):
        Set_Row_Address(i);
        Set_Column_Address(column);
        Write_Instruction(0x5C); 
        Data_processing(numberImages[16*value+i])
    
def adj_Contrast():
    
    Display_Picture(pic1)
    DrawString(6,0," Contrast level")
    
    while(True):
        number = (int(input("Enter a contrast value: ")))
    
        number1=number/100;
        number2=number%100/10;
        number3=number%100%10;
        Write_number(number1,0);
        Write_number(number2,2);
        Write_number(number3,4);    
    
        Write_Instruction(0xC1)
        Write_Data(number)    
    
def Display_Chess(value1,value2):
    Set_Row_Address(0)
    Set_Column_Address(0)       
    Write_Instruction(0x5c)    
    for i in xrange(32):
        for k in xrange(32):
            Data_processing(value1)
        for k in xrange(32):
            Data_processing(value2)    

def Gray_test():
    Set_Row_Address(0)
    Set_Column_Address(0)
    Write_Instruction(0x5c)
    
    for m in xrange(32):
        j = 0
        for k in xrange(16):
            for i in xrange(8):
                Write_Data(j)
            j = j + 0x11        
    
    for m in xrange(32):
        j = 255
        for k in xrange(16):
            for i in xrange(8):
                Write_Data(j)
            j = j - 0x11

def DrawString(x, y, pStr):
   for c in pStr:
        cc = ord(c)
            
        if cc>=0x80:
            DrawSpecialChar(x,y,cc)
            x = x + 4            
        else:
            DrawSingleAscii(x,y,cc)
            x = x + 2
            
def DrawSpecialChar(x, y, s):
    s = s - 0x80
    for i in xrange(16):
        Set_Row_Address(y+i)
        Set_Column_Address(x)
        Write_Instruction(0x5c)
        for k in xrange(2):
            Data_processing(specialChars[s*16+k+i*2])

def DrawSingleAscii(x, y, char):
    ofs = (char-32) * 16
    for i in xrange(16):
        Set_Row_Address(y+i)
        Set_Column_Address(x)
        Write_Instruction(0x5c)
        str = asciiImages[ofs + i]
        Data_processing(str)
        
def main():    
    print "Resetting display ..."
    resetOLED()
    
    print "Initializing display ..."
    Initial()

    print "All pixels on/off ..."
    Write_Instruction(0xa5) # --all display on
    time.sleep(1.0)
    Write_Instruction(0xa4) # --all Display off
    time.sleep(1.0)

    Write_Instruction(0xa6) # --set normal display    

    print "Picture 1 ..."
    Display_Picture(pic1)
    time.sleep(2.0)
    raw_input("ENTER")
    Write_Instruction(0xa7) # --set Inverse Display    
    time.sleep(2.0)
    raw_input("ENTER")
    Write_Instruction(0xa6) # --set normal display
    
    print "Picture 2 ..."
    Display_Picture(pic2)
    time.sleep(2.0)
    raw_input("ENTER")
    Write_Instruction(0xa7) # --set Inverse Display    
    time.sleep(2.0)
    raw_input("ENTER")
    Write_Instruction(0xa6) # --set normal display

    print "Credits ..."
    Display_Chess(0x00,0x00) # clear display
    DrawString(0, 0, "**** \x80\x81\x82\x83 ****")  
    DrawString(0, 16, "EASTRISING ")
    DrawString(0, 32, "WWW.BUY-DISPLAY.COM")
    DrawString(0, 48, "2013.04.22")
    time.sleep(2.0)
    raw_input("ENTER")

    print "Gray test ..."
    Gray_test() 
    time.sleep(2.0)
    raw_input("ENTER")
    
    print "Fill patterns ..."
    Display_Chess(0x55,0xaa)
    time.sleep(1.0)
    Display_Chess(0xaa,0x55)
    time.sleep(1.0)
    Display_Chess(0x55,0x55)
    time.sleep(1.0)
    Display_Chess(0xAA,0xAA)
    time.sleep(1.0)
    Display_Chess(0xFF,0x00)
    time.sleep(1.0)
    Display_Chess(0x00,0xFF)
    time.sleep(1.0)
    Display_Chess(0x00,0x00) # clear display
    time.sleep(1.0)
    
    print "Adjust contrast ..."    
    adj_Contrast()

if __name__ == "__main__":
    main()
    