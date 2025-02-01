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
m = rgbmatrix.RGBMatrix(width=64, height=32, bit_depth=5,rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
d = framebufferio.FramebufferDisplay(m, auto_refresh=False)
clr = 0.0
decclr = 0xffff00
con1 = ""
con2 = ""
def freshdate(dateobj):
    global con1,con2
    con1 = dateobj.strftime("%X")
    con2 = f"{dateobj.strftime('%d')}/{dateobj.strftime('%m')} {dateobj.strftime('%a')}"
def coloring():
    global decclr, clr
    clr += 0.01 #rainbow
    print(clr)
    r,g,b = colorsys.hsv_to_rgb(clr,1,1)
    print(f"{r};{g};{b}")
    r *= 0xff0000
    g *= 0xff00
    b *= 0xff
    print(f"{r}:{g}:{b}")
    r = round(r)
    g = round(g)
    b = round(b)
    print(f"rounded {r} {g} {b}")
    decclr = r+g+b
    print(decclr)
    print(hex(decclr))
dayclr = 0xffffff
def decideday(inputdate):
    global dayclr
    match int(inputdate.strftime("%w")):
        case 1:
            dayclr = 0xEE5555 #monday=danger
        case 2:
            dayclr = 0x5555EE #synesthesia
        case 3:
            dayclr = 0x888888 #dim white
        case 4:
            dayclr = 0xAA00EE #no synesthesia
        case 5:
            dayclr = 0x66ffcf #meenty
        case _:
            dayclr = 0xFFAA00 #orange
def blink(timeless):
    if (int(timeless.strftime("%S")) % 3 == 0):
        return 0
    else:
        return 1
#multiply with color to make text blink
coloring()
freshdate(datetime.datetime.now())
line1 = {}
line2 = {}
def linearthings():
    global line1, line2
    line1 = adafruit_display_text.label.Label(terminalio.FONT, text=f"time")
    line1.x = 2
    line1.y = 8
    line1.color = decclr
    line2 = adafruit_display_text.label.Label(terminalio.FONT,color=0xff00ff, text=f"date")
    line2.x = 2
    line2.y = 24
linearthings()
g = displayio.Group()
def groupie():
    global g
    g.append(line1)
    g.append(line2)
groupie()
d.root_group=g
alarm_hour = 7 #24hr time
alarm_minute_begin = 15
alarm_minute_end = 20 # example, blinks 7:15-7:20
def t(timeless, str):
    return int(timeless.strftime(str))
def testalarm(ti):
    if (alarm_hour == t(ti, "%H")):
        print("alarm hour")
        if (t(ti,"%M") >= alarm_minute_begin) and (t(ti,"%M") <= alarm_minute_end):
            print(f"alarm active {t(ti,"%M")} min")
            return 1*blink(ti)
        else:
            return 1
    else:
        return 1
while True:
    #dt = datetime.datetime(2025,2,1)
    # ^^ test day colors
    dt = datetime.datetime.now()
    freshdate(dt)
    coloring()
    decideday(dt)
    line1.text = con1
    line2.text = con2
    line1.color = decclr*testalarm(dt)
    line2.color = dayclr
    #linearthings()
    d.refresh(minimum_frames_per_second=5)
    #sleeping breaks this!!! what the devils?
    #actually nvm, its linearthings
    time.sleep(0.2)
