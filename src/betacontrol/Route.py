import numpy as np
import matplotlib.pyplot as plt

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

    DIRECTIONS = MANHATTAN_DIRECTIONS

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

    ORIGEN_MOVIMENT = np.array([0, 16])
    ORIGEN_IMATGE = np.array([72,1559])
    MIDA_QUADRAT = np.array([67,67])

    ENROC = {
        "60": np.array([14, 14]),
        "20": np.array([14, 0]),
        "67": np.array([0, 14]),
        "27": np.array([0, 0])
    }
    DEST_TORRE = {
        "60": np.array([14, 10]),
        "20": np.array([14, 6]),
        "67": np.array([0, 10]),
        "27": np.array([0, 6])
    }

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
        arribar a la casella de destinacio. Te en compte la natura del moviment.
        Les dades de retorns fan servir increments enters per representar les
        direccions del moviment, s'han d'escalar posteriorment a increments de
        motor o a increments d'imatge respectivament

        Parameters
        ----------
        move: str
            String que representa el moviment de manera compacta i independent
            d'estat del tauler (per minimitzar el solapament entre moduls)

        Returns
        -------
        list: np.ndarray
            Llista d'increments en les coordenades per dur a terme la ruta
        """
        full_route = []
        captura = True if "x" in move else False
        alpas = True if "e" in move else False
        coronacio = True if "=" in move else False
        enroc = True if "*" in move else False

        abs_origen = np.array([(7-int(move[1]))*2, (int(move[0]))*2])
        abs_dest = np.array([(7-int(move[3]))*2, (int(move[2]))*2])

        if enroc:
            posicio_torre = self.ENROC[move[2:4]]
            dest_torre = self.DEST_TORRE[move[2:4]]
            full_route += self.route_segment(self.ORIGEN_MOVIMENT, abs_origen, False)
            full_route += self.route_segment(abs_origen, abs_dest, True)
            full_route += self.route_segment(abs_dest, posicio_torre, False)
            full_route += self.route_segment(posicio_torre, dest_torre, True)
            full_route += self.route_segment(dest_torre, self.ORIGEN_MOVIMENT, False)
        else:
            if captura and not alpas:
                piece = move[move.find('x')+1]
                dest = self.find_empty_pos(piece)
                full_route += self.route_segment(self.ORIGEN_MOVIMENT, abs_dest, False)
                full_route += self.route_segment(abs_dest, dest, True)
                full_route += self.route_segment(dest, abs_origen, False)
                full_route += self.route_segment(abs_origen, abs_dest, True)
            elif captura and alpas:
                piece = move[move.find('x') + 1]
                dest = self.find_empty_pos(piece)
                alpas = np.array([dest[0], int(move[move.find('e')+1])])
                full_route += self.route_segment(self.ORIGEN_MOVIMENT, alpas, False)
                full_route += self.route_segment(alpas, dest, True)
                full_route += self.route_segment(dest, abs_origen, False)
                full_route += self.route_segment(abs_origen, abs_dest, True)
            elif not enroc:
                full_route += self.route_segment(self.ORIGEN_MOVIMENT, abs_origen, False)
                full_route += self.route_segment(abs_origen, abs_dest, True)

            if coronacio:
                piece = move[move.find("=")+1]
                dest_pawn = self.find_empty_pos('P' if piece.isupper() else 'p')
                dest_dead = self.find_dead_piece(piece)
                full_route += self.route_segment(abs_dest, dest_pawn, True)
                full_route += self.route_segment(dest_pawn, dest_dead, False)
                full_route += self.route_segment(dest_dead, abs_dest, True)

            full_route += self.route_segment(abs_dest, self.ORIGEN_MOVIMENT, False)
        return full_route

    def route_matrix(self, origin: np.ndarray, destination: np.ndarray, magnet: bool = False):
        """
        Algorisme de Wavefront (Dijkstra) per trobar la ruta amb menys passos
        (la qual cosa implica que nomes es optim en distancia euclidiana si
        s'utilitza amb direccions de manhattan)

        Considera les caselles ocupades per les peces mortes i traça rutes
        evitant col·lisions. Es pot millorar perque pugui considerar les
        peces del tauler també.

        Parameters
        ----------
        origin: np.ndarray
            Vector amb l'origen amb la convenció de la matriu (veure imatge
            a la carpeta datasets)
        destination: np.ndarray
            Vector amb l'origen amb la convenció de la matriu
        magnet: bool
            Si està a true evadeix les peces del tauler. Sino no cal

        Returns
        -------
        np.ndarray
            Matriu de Wavefront fins el punt d'arribada (no es completa al
            100% per estalviar en recursos)
        """
        wavefront_matrix = np.zeros(self.WAVEFRONT_SIZE, dtype=np.int)

        if magnet:
            wavefront_matrix += self.WAVEFRONT_MAGNET + self.set_occupied()

        wavefront_matrix[origin[0], origin[1]] = 2
        wavefront_matrix[destination[0], destination[1]] = 0

        move_heap = [origin + direction for direction in self.DIRECTIONS
                     if not np.any(self.WAVEFRONT_ZERO > origin + direction)
                     and not np.any(origin + direction >= self.WAVEFRONT_SIZE)]
        move_heap = [move for move in move_heap if np.all(wavefront_matrix[move[0], move[1]] == 0)]

        for move in move_heap:
            wavefront_matrix[move[0], move[1]] = 3

        while move_heap != []:
            position = move_heap.pop()
            moves = [position + direction for direction in self.DIRECTIONS
                     if not np.any(self.WAVEFRONT_ZERO > position + direction)
                     and not np.any(position + direction >= self.WAVEFRONT_SIZE)]
            moves = [move for move in moves if np.all(wavefront_matrix[move[0], move[1]] == 0)]

            for move in moves:
                if wavefront_matrix[move[0], move[1]] == 0:
                    wavefront_matrix[move[0], move[1]] = wavefront_matrix[position[0], position[1]] + 1
                if np.all(move == destination):
                    return wavefront_matrix

            move_heap = moves + move_heap
        return None

    def route_segment(self, origin: np.ndarray, destination: np.ndarray, magnet: bool):
        """
        Troba un segment de ruta entre un origen i una destinació (coordenades
        en format Convenció Matriu, veure imatge a Datasets)

        Parameters
        ----------
        origin: np.ndarray
            Coordenades de l'origen del moviment
        destination: np.ndarray
            Coordenades de la destinació
        magnet: bool
            Si està a True eludirà les peces sobre el tauler

        Returns
        -------
        list: np.ndarray
            Llista de passos a seguir per arribar de l'origen a la destinació
            (codificats com a vectors de la forma [x, y] on x,y [-{-1, 0, 1})
        """
        matrix = self.route_matrix(origin, destination, magnet)
        position = np.copy(destination)
        route = []

        while not np.all(position == origin):
            moves = [direction for direction in self.DIRECTIONS
                     if not np.any(self.WAVEFRONT_ZERO > position + direction)
                     and not np.any(position + direction >= self.WAVEFRONT_SIZE)]
            step = [move for move in moves if np.all(matrix[(position+move)[0],
                                                            (position+move)[1]] == matrix[position[0], position[1]] - 1)][0]
            route.insert(0,-step)
            position += step
        return route

    def set_occupied(self) -> np.ndarray:
        """
        Genera una matriu de màscara per a determinar les caselles ocupades
        per peces mortes a la banda del tauler.

        Returns
        -------
        np.ndarray
            Matriu de zeros de mida SIZE_WAVEFRONT amb les caselles ocupades en
            forma de números 1
        """
        occuppied = np.zeros(self.WAVEFRONT_SIZE, dtype=np.int)
        for i in range(self.capture_map.shape[0]):
            for j in range(self.capture_map.shape[1]):
                if self.capture_map[i, j]:
                    occuppied[2*j, i + 16] = 1
        return occuppied

    def draw_route(self, route: list, board_image: np.ndarray):
        """
        Representa el moviment sobre una de les imatges del dataset (calibrat
        amb els renders de /datasets/early-test

        Parameters
        ----------
        route: list: np.ndarray
            Llista de moviments codificats com l'output de route_calculate
        board_image: np.ndarray
            Imatge sobre la qual dibuixar el moviment
        """
        plt.figure(figsize=(12, 8))
        plt.imshow(board_image)
        current_position = np.copy(self.ORIGEN_IMATGE)
        for num, i in enumerate(route):
            increment = np.multiply(i, self.MIDA_QUADRAT)
            plt.arrow(current_position[1], current_position[0], increment[1], increment[0], shape="left",
                      length_includes_head=True, width=0.5, color='b')
            plt.text(current_position[1] - 25, current_position[0], str(num), color='b')
            current_position = current_position + increment
        plt.show()


    def find_empty_pos(self, symbol: str) -> np.ndarray:
        """
        Troba una posició buida a la qual emplaçar una peça morta, la retorna
        i la configura com a ocupada.

        Parameters
        ----------
        symbol: str
            Símbol de la peça que es vol prendre

        Returns
        -------
        np.ndarray
            Coordenades on emplaçar la peça
        """
        for i in self.PIECE_POSITIONS[symbol]:
            if not self.capture_map[i[0], i[1]]:
                self.capture_map[i[0], i[1]] = True
                return np.array([i[1]*2, i[0] + 16])


    def find_dead_piece(self, symbol: str):
        """
        Troba una casella on hi ha una peça morta (per a les promocions), la
        retorna i la configura com a lliure

        Parameters
        ----------
        symbol: str
            Símbol de la peça

        Returns
        -------
        np.ndarray
            Coordenades de la peça
        """
        for i in self.PIECE_POSITIONS[symbol]:
            if self.capture_map[i[0], i[1]]:
                self.capture_map[i[0], i[1]] = False
                return np.array([i[1] * 2, i[0] + 16])
        return None