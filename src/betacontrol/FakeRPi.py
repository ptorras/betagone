HIGH = 1
LOW = 0
BCM = "numbering mode"
mode = "default"
OUT = "output"


def output(pin, value):
    print("send to GPIO pin: " + str(pin) + " the value of: " + str(value))

def setmode(mode):
    print("The mode used is:" + str(mode))

def setup(pin, mode):
    print("sets the GPIO pin num: " + str(pin) + " as " + str(mode) + " pin")

def cleanup():
    print("clean the linked GPIO pins")

