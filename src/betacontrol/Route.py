import numpy as np

class Route:
    DIR_NORTH = np.array([ 0,  1])
    DIR_SOUTH = np.array([ 0, -1])
    DIR_EAST  = np.array([ 1,  0])
    DIR_WEST  = np.array([-1,  0])

    DIR_NE = np.array([ 1,  1])
    DIR_NW = np.array([-1,  1])
    DIR_SE = np.array([ 1, -1])
    DIR_SW = np.array([-1, -1])

    MANHATTAN_DIRECTIONS = [DIR_NORTH, DIR_EAST, DIR_SOUTH, DIR_WEST]
    FULL_DIRECTIONS = [DIR_NORTH, DIR_NE, DIR_EAST, DIR_SE, DIR_SOUTH, DIR_SW, DIR_WEST, DIR_NW]

    PIECE_POSITIONS = {
        "p": [(2, x) for x in range(8)],
        "n": [(3, 1), (3, 6)],
        "b": [(3, 2), (3, 5)],
        "r": [(3, 0), (3, 7)],
        "q": [(3, 3)],
        "k": [(3, 4)],
        "P": [(0, x) for x in range(8)],
        "N": [(1, 1), (1, 6)],
        "B": [(1, 2), (1, 5)],
        "R": [(1, 0), (1, 7)],
        "Q": [(1, 3)],
        "K": [(1, 4)],
    }

    def __init__(self, status:str):
        """
        Inicialitza l'estat de l'objecte per a considerar les peces que s'han
        tret del tauler

        Parameters
        ----------
        status: str
            String FEN amb el contingut de la primera posicio del tauler
        """
        self.capture_map = np.zeros((4, 8), dtype=np.bool)

        for ch in status:
            if ch == ' ':
                break
            if ch in "pnbrqkPNBRQK":
                for i in self.PIECE_POSITIONS[ch]:
                    if not self.capture_map[i[0], i[1]]:
                        self.capture_map[i[0], i[1]] = True
                        break
        self.capture_map = np.logical_not(self.capture_map)

    def calculate(self, move:str):
        pass