'''
  *  The MIT License (MIT)
  *
  *  G213Colors v0.3 Copyright (c) 2016, 2017, 2018 SebiTimeWaster
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
import binascii
import randomcolor


standardColorHex = 'ffb4aa'         # Standard color, i found this color to produce a white color on my G213
idVendor         = 0x046d           # The id of the Logitech company
idProduct        = 0xc336           # The id of the G213
bEndpointAddress = 0x82             # Endpoint to read data back from
bmRequestType    = 0x21             # --.
bmRequest        = 0x09             #    \ The controll transfer
wValue           = 0x0211           #    / configuration for the G213
wIndex           = 0x0001           # --'
colorCommand     = '11ff0c3a{}01{}0200000000000000000000'   # binary commands in hex format, always 20 byte long
breatheCommand   = '11ff0c3a0002{}{}006400000000000000'
cycleCommand     = '11ff0c3a0003ffffff0000{}64000000000000'
device           = ''               # device resource
isDetached       = False            # If kernel driver needs to be reattached
numArguments     = len(sys.argv)    # number of arguments given
option           = ''


def connectG():
    global device, isDetached
    # find G product
    device = usb.core.find(idVendor = idVendor, idProduct = idProduct)
    # if not found exit
    if device is None:
        print('USB device not found!')
        sys.exit(1)
    # if a kernel driver is attached to the interface detach it, otherwise no data can be send
    if device.is_kernel_driver_active(wIndex):
        device.detach_kernel_driver(wIndex)
        isDetached = True

def disconnectG():
    # free device resource to be able to reattach kernel driver
    usb.util.dispose_resources(device)
    # reattach kernel driver, otherwise special keys will not work
    if isDetached:
        device.attach_kernel_driver(wIndex)

def checkColorHex(colorHex):
    try:
        if len(colorHex) != 6:
            raise ValueError()
        int(colorHex, 16)
    except:
        pass
        print('Not a valid hexadecimal color!')
        return False
    return True

def checkSpeedNum(numStr):
    try:
        num = int(numStr)
        if num < 32 or num > 65535:
            raise ValueError()
    except:
        pass
        print('Not a valid time in milliseconds!')
        return False
    return True

def sendData(dataHex):
    # convert hex data to binary and send it
    device.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataHex))
    # read back one 20-byte word, otherwise commands may not be completely executed
    device.read(bEndpointAddress, 20)

def sendColorCommand(colorHex, field = 0):
    if checkColorHex(colorHex):
        # convert number to hex
        fieldHex = format(field, '02x')
        commandHex = colorCommand.format(fieldHex, colorHex)
        sendData(commandHex)

def sendBreatheCommand(colorHex, speed):
    if checkColorHex(colorHex) and checkSpeedNum(speed):
        # convert number to hex
        speedHex = format(int(speed), '04x')
        commandHex = breatheCommand.format(colorHex, speedHex)
        sendData(commandHex)

def sendCycleCommand(speed):
    if checkSpeedNum(speed):
        # convert number to hex
        speedHex = format(int(speed), '04x')
        commandHex = cycleCommand.format(speedHex)
        sendData(commandHex)

def getRandomColor():
    return randomcolor.RandomColor().generate()[0][1:]

def setRandomColor():
    colorHex = getRandomColor()
    sendColorCommand(colorHex)

def setRandomColorSegments():
    for i in range(1, 6):
        sendColorCommand(getRandomColor(), i)

def printInfo():
    print('G213Colors - Changes the key colors on a Logitech G213 Prodigy Gaming Keyboard')
    print('')
    print('Options:')
    print('-c                         Set the standard color (white)')
    print('-c  <color>                Set a custom color')
    print('-c  <color1> ... <color5>  Set custom colors for all 5 segments')
    print('-b  <color> <time>         Sets a color breathing animation')
    print('-x  <time>                 Sets a color cycling animation')
    print('-ra                        Sets a random color for whole keyboard')
    print('-rs                        Sets different random color for every segment')
    print('')
    print('Please note:')
    print('* Color is a hex encoded color in the format RRGGBB')
    print('  i.e. ff0000 is red, 00ff00 is green and so on,')
    print('  abbreviated formats are not allowed')
    print('* Time is in milliseconds in the range of 32 to 65535')


# option to use
if numArguments > 1:
    option = str(sys.argv[1])
# if no option found, exit
if '-' not in option:
    printInfo()
    sys.exit(1)

connectG()

# send command depending on option used and argument count
if 'c' in option:
    if numArguments == 2:
        sendColorCommand(standardColorHex)
    elif numArguments == 3:
        sendColorCommand(sys.argv[2])
    elif numArguments == 7:
        for index in range(1, 6):
            sendColorCommand(sys.argv[index + 1], index)
    else:
        printInfo()
elif 'b' in option and numArguments == 4:
    sendBreatheCommand(sys.argv[2], sys.argv[3])
elif 'x' in option and numArguments == 3:
    sendCycleCommand(sys.argv[2])
elif 'ra' in option and numArguments == 2:
    setRandomColor()
elif 'rs' in option and numArguments == 2:
    setRandomColorSegments()
else:
    printInfo()

disconnectG()
