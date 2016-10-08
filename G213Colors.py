'''
  *  The MIT License (MIT)
  *
  *  G213Colors v0.1 Copyright (c) 2016 SebiTimeWaster
  *
  *  Permission is hereby granted, free of charge, to any person obtaining a copy
  *  of this software and associated documentation files (the "Software"), to deal
  *  in the Software without restriction, including without limitation the rights
  *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  *  copies of the Software, and to permit persons to whom the Software is
  *  furnished to do so, subject to the following conditions:
  *
  *  The above copyright notice and this permission notice shall be included in all
  *  copies or substantial portions of the Software.
  *
  *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  *  SOFTWARE.
'''


import sys
import usb.core
import usb.util
from time import sleep


standardColor  = 'ffb4aa'         # Standard color, i found this color to produce a white color on my G213
idVendor       = 0x046d           # The id of the Logitech company
idProduct      = 0xc336           # The id of the G213
bmRequestType  = 0x21             # --.
bmRequest      = 0x09             #    \ The controll transfer
wValue         = 0x0211           #    / configuration for the G213
wIndex         = 0x0001           # --'
colorCommand   = "11ff0c3a{}01{}0200000000000000000000"   # binary commands in hex format
breatheCommand = "11ff0c3a0002{}{}006400000000000000"
cycleCommand   = "11ff0c3a0003ffffff0000{}64000000000000"
device         = ""               # device resource
isDetached     = False            # If kernel driver needs to be reattached
numArguments   = len(sys.argv)    # number of arguments given
if numArguments > 1:
    option     = str(sys.argv[1]) # option to use
else:
    option     = ""


def connectG():
    global device, isDetached
    # find G product
    device = usb.core.find(idVendor = idVendor, idProduct = idProduct)
    # if not found exit
    if device is None:
        raise ValueError("USB device not found!")
    # if a kernel driver is attached to the interface detach it, otherwise no data can be send
    if device.is_kernel_driver_active(wIndex):
        device.detach_kernel_driver(wIndex)
        isDetached = True

def disconnectG():
    # free device resource to be able to reattach kernel driver
    usb.util.dispose_resources(device)
    # reattach kernel driver, otherwise special key will not work
    if isDetached:
        device.attach_kernel_driver(wIndex)

def sendData(data):
    device.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, data)

def sendColorCommand(colorHex, field = 0):
    # create command, decode it to binary and send it
    sendData(colorCommand.format(str(format(field, '02x')), colorHex).decode("hex"))

def sendBreatheCommand(colorHex, speed):
    sendData(breatheCommand.format(colorHex, str(format(speed, '04x'))).decode("hex"))

def sendCycleCommand(speed):
    sendData(cycleCommand.format(str(format(speed, '04x'))).decode("hex"))

def printInfo():
    print "G213Colors - Changes the key colors on a Logitech G213 Prodigy Gaming Keyboard"
    print "\nOptions:"
    print "-c                        Set the standard color (white)"
    print "-c <color>                Set a custom color"
    print "-c <color1> ... <color5>  Set custom colors for the 5 segments"
    print "-b <color> <time>         Sets a color breathing animation"
    print "-x <time>                 Sets a color cycling animation"
    print "\nPlease note:"
    print "* Color is a hex encoded color in the format RRGGBB"
    print "  i.e. ff0000 is red, 00ff00 is green and so on,"
    print "  abbreviated formats are not allowed"
    print "* Time is in milliseconds, range: 32 - 65535"


if "-" not in option:
    # no option found, exit
    printInfo()
    sys.exit(1)

connectG()

if "c" in option:
    if numArguments == 2:
        sendColorCommand(standardColor)
    elif numArguments == 3:
        sendColorCommand(str(sys.argv[2]))
    elif numArguments == 7:
        for index in range(1, 6):
            sendColorCommand(str(sys.argv[index + 1]), index)
            sleep(0.01)
    else:
        printInfo()
elif "b" in option and numArguments == 4:
    sendBreatheCommand(str(sys.argv[2]), int(sys.argv[3]))
elif "x" in option and numArguments == 3:
    sendCycleCommand(int(sys.argv[2]))
else:
    printInfo()

disconnectG()
