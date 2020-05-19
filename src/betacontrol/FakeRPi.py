class GPIO:
    def __init__(self):
        pass

    def output(self, pin, value):
        print("send to GPIO pin: " + pin + " the value of: " + value)

    def setmode(self, mode):
        print("The mode used is:" + mode)

    def setup(self, pin):
        print("sets the GPIO pin num: " + pin + " as an output pin")

    def cleanup(self):
        print("clean the linked GPIO pins")

    HIGH = 1
    LOW = 0
    BCM = "numbering mode"
    mode = "default"
    OUT = "output"
