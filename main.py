from machine import Pin, PWM
from rotary import Rotary
import utime as time
import framebuf
import base64
import ssd1306

print("GurgleApps.com Frequency Generator")
use_i2c_oled_screen = True
# Configure GPIO pin for frequency output
freq_pin = 3
# rotary encoder
rotary_dt = 0
rotary_clk = 1
rotary_sw = 2
# i2c oled display
ssd_clock_pin = 5
ssd_data_pin = 4
ssd_bus = 0

freq = 20
logo_large = b'gB//8A////AP///wD///8A///4AB//+AAf//gAH//4AB//wAAD/8AAA//AAAP/wAAD/gAAAH4AAAB+AAAAfgAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAMAAAAAAAAAB4AAAAAAAAAHgAAAAAABgAeAAAAAAAAADwAAAAAAAYAFhgAAAAAAAHcAA4AAwZGADYYAAAHHAABwAAfAB8PxgA2HyAADz7AA94AH4CfjMYAMxswABs68AG8ABmMmQzGDiMZvBwYMvsA/QAZjJgMxh4/Gb4+GDP/g/wAMIyYDMYTPxmzNBgzz4B8ADCMmAzGN3sZszAZM8yDxQAwDJgExj5jmbM8GxPMgdwAM4yYB8YwYZ+zHh8fzMHdADPN2AfGMmAfswbMDszB3QARz9gAxjZgGzsmwADMwZ0AGY6ADMYeABg/PIAATMWdAB+AAATCGAAYNzgAAAzBnQAPgAAHwAAAGDAAAAAAxZ0ABwAAA8AAAAAwAAAAAA2cAAAAAAAAAAAAMAAAAAABgDgAAAH4AAAB+BAAAfgAAAH/AAAP/wAAD/8AAA//AAAP//AA///wAP//8AD///AA///+B////gf///4H///+B//'
pwm = PWM(Pin(freq_pin))
pwm.freq(freq)
pwm.duty_u16(int(65535/2))
display = None
logo_large_buff = None
generating = True
rotary = Rotary(rotary_dt,rotary_clk,rotary_sw)
    

def rotary_changed(change):
    global freq, pwm, generating
    if change == Rotary.ROT_CW:
        freq = freq + 1
        print(freq)
    elif change == Rotary.ROT_CCW:
        freq = freq - 1
        print(freq)
    elif change == Rotary.SW_PRESS:
        print('PRESS')
    elif change == Rotary.SW_RELEASE:
        generating = not generating
        pwm.duty_u16(0)
    update_freq(freq)

def update_freq(f):
    freq = f
    pwm.freq(freq)
    pwm.duty_u16(0)
    if generating:
        pwm.duty_u16(int(65535/2))
    if (use_i2c_oled_screen):
        update_i2c_display()
    
def custom_to_buff(data):
    width = data[0]
    height = data[1]
    fbuff = framebuf.FrameBuffer(data[2:],width,height, framebuf.MONO_HLSB)
    return fbuff

def setup_i2c_display():
    global display, logo_large_buff
    i2c = machine.I2C(ssd_bus,sda=machine.Pin(ssd_data_pin),scl=machine.Pin(ssd_clock_pin))
    display = ssd1306.SSD1306_I2C(128,64,i2c)
    logo_large_buff = custom_to_buff(bytearray(base64.b64decode(logo_large)))
    display.blit(logo_large_buff, 0, 0)
    display.show()
    
def update_i2c_display():
    display.blit(logo_large_buff, 0, 0)
    freq_text_y = 36
    generating_text_y = 50
    display.fill_rect(0,freq_text_y,128,10,0)
    display.text("Freq: "+str(freq)+"Hz",0,freq_text_y)
    display.fill_rect(0,generating_text_y,128,10,0)
    display.text("Generating:"+str(generating),0,generating_text_y)
    display.show()
    
rotary.add_handler(rotary_changed)

if (use_i2c_oled_screen):
    setup_i2c_display()
    time.sleep(1)
    update_i2c_display()

while True:
        time.sleep(0.1)

