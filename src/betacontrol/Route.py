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

    WAVEFRONT_ZERO = np.array([0, 0])
    WAVEFRONT_SIZE = np.array([15, 20])
    WAVEFRONT_MAGNET = np.array([[1 if x % 2 == 0 and x < 0 else 0 for x in range(-16,4)]
                                 if x % 2 == 0 else [0 for y in range(-16, 4)] for x in range(0, 15)],
                                dtype=np.int)

    def __init__(self, status: str):
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

    def route_calculate(self, move: str):
        """
        Utilitza una representacio wavefront per trobar el cami mes rapid per
        arribar a la casella de destinacio. Te en compte la natura del moviment
        i es genera unicament amb connectivitat a 4.

        Parameters
        ----------
        move: str
            String que representa el moviment de manera compacta i independent
            d'estat del tauler (per minimitzar el solapament entre moduls)

        Returns
        -------

        """
        captura = True if "x" in move else False
        alpas = True if "e" in move else False
        coronacio = True if "=" in move else False
        enroc = True if "*" in move else False

    def route_matrix(self, origin: np.ndarray, destination: np.ndarray, magnet: bool = False):
        wavefront_matrix = np.zeros(self.WAVEFRONT_SIZE, dtype=np.int)

        if magnet:
            wavefront_matrix += self.WAVEFRONT_MAGNET + self.set_occupied()

        wavefront_matrix[origin[0], origin[1]] = 2
        move_heap = [origin + direction for direction in self.FULL_DIRECTIONS
                     if not np.any(self.WAVEFRONT_ZERO > origin + direction)
                     and not np.any(origin + direction > self.WAVEFRONT_SIZE)]
        move_heap = [move for move in move_heap if np.all(wavefront_matrix[move[0], move[1]] == 0)]

        for move in move_heap:
            wavefront_matrix[move[0], move[1]] = 3

        while move_heap != []:
            position = move_heap.pop()
            moves = [position + direction for direction in self.FULL_DIRECTIONS
                     if not np.any(self.WAVEFRONT_ZERO > position + direction)
                     and not np.any(position + direction > self.WAVEFRONT_SIZE)]
            moves = [move for move in moves if np.all(wavefront_matrix[move[0], move[1]] == 0)]

            for move in moves:
                if wavefront_matrix[move[0], move[1]] == 0:
                    wavefront_matrix[move[0], move[1]] = wavefront_matrix[position[0], position[1]] + 1
                if np.all(move == destination):
                    return wavefront_matrix

            move_heap = moves + move_heap
        return None

    def route_segment(self, origin: np.ndarray, destination: np.ndarray, magnet: bool):
        matrix = self.route_matrix(origin, destination, magnet)
        position = destination
        route = []

        while not np.all(position == origin):
            moves = [direction for direction in self.FULL_DIRECTIONS
                     if not np.any(self.WAVEFRONT_ZERO > position + direction)
                     and not np.any(position + direction > self.WAVEFRONT_SIZE)]
            step = [move for move in moves if np.all(matrix[(position+move)[0],
                                                            (position+move)[1]] == matrix[position[0], position[1]] - 1)][0]
            route.append(step)
            position += step
        return route

    def set_occupied(self) -> np.ndarray:
        occuppied = np.zeros(self.WAVEFRONT_SIZE, dtype=np.int)
        for i in range(self.capture_map.shape[0]):
            for j in range(self.capture_map.shape[1]):
                if self.capture_map[i, j]:
                    occuppied[2*j, i + 16] = 1
        return occuppied


    def draw_route(self, route: list, board_image: np.ndarray):
        pass