#64x32 display with a rainbow animation, probably a clock function too
import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import colorsys
import time
import datetime
displayio.release_displays()
m = rgbmatrix.RGBMatrix(width=64, height=32, bit_depth=4,rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
d = framebufferio.FramebufferDisplay(m, auto_refresh=False)
clr = 0.0
hexclr= 0xffffff
con1 = ""
con2 = ""
def freshdate(dateobj):
    global con1,con2
    con1 = dateobj.strftime("%X")
    con2 = f"{dateobj.strftime('%d')}/{dateobj.strftime('%m')} {dateobj.strftime('%a')}"
def coloring():
    global hexclr
    clr += 0.1 #rainbow
    r,g,b = colorsys.hsv_to_rgb(clr,1,1)
    hexclr = int(hex(r*256^3+g*256^2+b*256))
coloring()
freshdate(datetime.datetime.now())
line1 = adafruit_display_text.label.Label(terminalio.FONT,color=hexclr, text=con1)
line1.x = d.width
line1.y = 8
line2 = adafruit_display_text.label.Label(terminalio.FONT,color=0xffffff, text=con2)
line2.x = d.width
line1.y = 24
g = displayio.Group()
g.append(line1)
g.append(line2)
d.root_group = g
while True:
    freshdate(datetime.datetime.now())
    coloring()
    d.refresh(minimum_frames_per_second=0)
    time.sleep(0.2)