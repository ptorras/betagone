from time import sleep
import FakeRPi as GPIO
import numpy as np

class Movement:

    def __init__(self):
        pass

    def do_one_step_lineal(self, motor, direction):

        GPIO.output(motor["DIR"], direction)
        for x in range(self.step_count):
            GPIO.output(motor["STEP"], GPIO.HIGH)
            GPIO.output(motor["STEP"], GPIO.LOW)

    def do_one_step_diagonal(self, direction1, direction2):

        GPIO.output(self.MOTOR1["DIR"], direction1)
        GPIO.output(self.MOTOR2["DIR"], direction2)
        for x in range(self.step_count):
            GPIO.output(self.MOTOR1["STEP"], GPIO.HIGH)
            GPIO.output(self.MOTOR2["STEP"], GPIO.HIGH)
            GPIO.output(self.MOTOR1["STEP"], GPIO.LOW)
            GPIO.output(self.MOTOR2["STEP"], GPIO.LOW)

    def print_board(self):
        self.board = self.clearBoard
        self.board[self.posXMagnet, self.posYMagnet] = self.posMagnet
        print(self.board)
        print("")

    def move_to(self, destination):

        coord_x = destination[0]
        coord_y = destination[1]

        if coord_x != 0 and coord_y != 0:
            self.do_one_step_diagonal(self.get_direction(coord_x), self.get_direction(coord_y))
            self.posXMagnet += coord_x
            self.posYMagnet += coord_y
        elif coord_y == 0:
            self.do_one_step_lineal(self.MOTOR1, self.get_direction(coord_x))
            self.posXMagnet += coord_x
        elif coord_x == 0:
            self.do_one_step_lineal(self.MOTOR2, self.get_direction(coord_y))
            self.posYMagnet += coord_y
        self.print_board()

    def get_direction(self, valor):
        if valor == -1:
            return self.BACK
        elif valor == 1:
            return self.FW

    def cleanup(self):
        GPIO.cleanup()

    def make_route(self, positions, magnet):
        mag_on = False
        for pos, mag in zip(positions, magnet):
            self.move_to(pos)
            if mag_on != mag:
                mag_on = not mag_on
                print("IMANT " + "on" if mag_on else "off")

    MOTOR1 = {
        "DIR": 20,  # Direction GPIO pin
        "STEP": 21,  # Step GPIO pin
        "ID": 1,
        "DESC": "Jumps between rows"
    }
    MOTOR2 = {
        "DIR": 14,  # Direction GPIO pin
        "STEP": 15,  # Step GPIO pin
        "ID": 2,
        "DESC": "Jumps between columns"
    }

    FW = 1  # Direction of the movement
    BACK = 0  # Direction of the movement
    SPR = 200  # Steps per Revolution
    HALF = 100  # Half of the revolution

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR1["DIR"], GPIO.OUT)
    GPIO.setup(MOTOR1["STEP"], GPIO.OUT)
    GPIO.setup(MOTOR2["DIR"], GPIO.OUT)
    GPIO.setup(MOTOR2["STEP"], GPIO.OUT)

    step_count = HALF

    clearBoard = np.array([["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "],
                           ["---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---", "-+-", "---",
                            "-+-", "---", "-| ", "   ", "   ", "   ", "   "],
                           ["   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ", " | ", "   ",
                            " | ", "   ", " | ", "   ", "   ", "   ", "   "]])
    board = clearBoard

    # The positions of the board makes it a 20x15
    # The X marks the spot where the magnet is

    posMagnet = "| X |"
    iniXMagnet = 0
    iniYMagnet = 16
    posXMagnet = iniXMagnet
    posYMagnet = iniYMagnet
    GPIO.cleanup()